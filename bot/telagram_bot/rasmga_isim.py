import logging
import aiohttp
import io

from aiogram import Router, types
from aiogram.types import BufferedInputFile
from PIL import Image, ImageDraw, ImageFont
from bot.telagram_bot.buttons import create_name_role_buttons, create_image_buttons

router = Router()
logger = logging.getLogger(__name__)

user_states = {}


@router.callback_query(lambda call: call.data == 'image_for_name')
async def show_name_roles(call: types.CallbackQuery):
    buttons = await create_name_role_buttons()
    await call.message.edit_text("Isimlardan birini tanlang", reply_markup=buttons)


# Example of how you would use these functions in your bot handlers
@router.callback_query(lambda call: call.data.startswith('role_'))
async def show_images_for_role(call: types.CallbackQuery):
    role_id = int(call.data.split('_')[1])
    logger.debug(f"Selected role_id: {role_id}")
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
                                font = ImageFont.truetype("timesbd.ttf", 85)  # Agar font yo'q bo'lsa, boshqa fontni tanlang
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
