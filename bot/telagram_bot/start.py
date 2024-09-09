import logging
import aiohttp
import io

from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.utils.markdown import bold
from bot.telagram_bot.majburiy_azolik import create_channels_buttons, fetch_channels, check_membership
from bot.telagram_bot.user_create import save_user_data
from bot.telagram_bot.buttons import home_buttons, create_image_buttons, create_name_role_buttons
from PIL import Image, ImageDraw, ImageFont
from aiogram.types import BufferedInputFile

router = Router()
logger = logging.getLogger(__name__)

user_states = {}


@router.message(CommandStart())
async def send_welcome(message: types.Message):
    user_data = {
        "telegram_id": message.from_user.id,
        "name": message.from_user.full_name,
        "username": message.from_user.username
    }

    status = await save_user_data(user_data)

    if status in (200, 201):
        buttons = await create_channels_buttons()
        await message.answer(
            bold("Botdan foydalanish uchun kanallarga azo bo'ling"),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=buttons
        )
    else:
        await message.answer("Foydalanuvchi ma'lumotlarini saqlashda xatolik yuz berdi.")
        logger.error(f"Failed to save user data: {user_data}")


@router.callback_query(lambda call: call.data == "check_subscription")
async def check_subscription(call: types.CallbackQuery):
    user_id = call.from_user.id
    channels = fetch_channels()

    all_members = True
    for channel in channels:
        is_member = await check_membership(user_id, channel['channel_id'])
        if not is_member:
            all_members = False
            await call.message.answer(f"Siz {channel['name']} kanaliga azo emassiz. Iltimos, kanalga azo bo'ling.")

    if all_members:
        buttons = await home_buttons()
        await call.message.edit_text("Xizmatlardan birini tanlang", reply_markup=buttons)
    else:
        buttons = await create_channels_buttons()
        await call.message.edit_text(
            bold("Siz hali hamma kanallarga azo bo'lmadingiz. Iltimos, avval azo bo'ling."),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=buttons
        )


@router.callback_query(lambda call: call.data == 'image_for_name')
async def show_name_roles(call: types.CallbackQuery):
    buttons = await create_name_role_buttons()
    await call.message.edit_text("Isimlardan birini tanlang", reply_markup=buttons)


@router.callback_query(lambda call: call.data.startswith('role_'))
async def show_images_for_role(call: types.CallbackQuery):
    role_id = int(call.data.split('_')[1])
    buttons = await create_image_buttons(role_id)
    await call.message.edit_text("Rasmlardan birini tanlang", reply_markup=buttons)


@router.callback_query(lambda call: call.data.startswith('image_'))
async def ask_for_name(call: types.CallbackQuery):
    image_id = int(call.data.split('_')[1])
    user_id = call.from_user.id
    user_states[user_id] = {"state": "awaiting_name", "image_id": image_id}
    await call.message.answer("Ismingizni kiriting:")


@router.message()
async def receive_name_and_show_image(message: types.Message):
    user_id = message.from_user.id
    if user_id in user_states and user_states[user_id]["state"] == "awaiting_name":
        name = message.text
        image_id = user_states[user_id]["image_id"]
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://127.0.0.1:8000/api/images/{image_id}/', ssl=False) as response:
                if response.status == 200:
                    image_data = await response.json()
                    image_url = image_data['image_url']
                    logger.debug(f"Fetched image URL: {image_url}")

                    async with session.get(image_url) as img_response:
                        if img_response.status == 200:
                            img_bytes = await img_response.read()
                            img = Image.open(io.BytesIO(img_bytes))

                            # Matnni oq rangda rasmga qo'shish
                            draw = ImageDraw.Draw(img)
                            try:
                                font = ImageFont.truetype("timesbd.ttf", 85)
                            except IOError:
                                font = ImageFont.load_default()

                            text_bbox = draw.textbbox((0, 0), name, font=font)
                            text_width = text_bbox[2] - text_bbox[0]
                            text_height = text_bbox[3] - text_bbox[1]
                            image_width, image_height = img.size
                            x_position = (image_width - text_width) // 2  # Center horizontally
                            y_position = 980
                            text_position = (x_position, y_position)
                            text_color = "white"

                            draw.text(text_position, name, font=font, fill=text_color)

                            img_byte_arr = io.BytesIO()
                            img.save(img_byte_arr, format='PNG')
                            img_byte_arr.seek(0)

                            input_file = BufferedInputFile(img_byte_arr.read(), filename="image.png")
                            await message.answer_photo(photo=input_file)
                        else:
                            await message.answer("Rasmni yuklashda xatolik yuz berdi.")
                else:
                    await message.answer("Rasmni yuklashda xatolik yuz berdi.")
        user_states.pop(user_id)
    else:
        await message.answer("Iltimos, to'g'ri ismni kiriting.")
