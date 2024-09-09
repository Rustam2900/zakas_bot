from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.utils.markdown import bold
from bot.telagram_bot.majburiy_azolik import create_channels_buttons, check_user_subscription
from bot.telagram_bot.user_create import save_user_data
from bot.telagram_bot.buttons import home_buttons  # Import the home_buttons function
import logging

router = Router()
logger = logging.getLogger(__name__)

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
        await message.answer("Foydalanuvchi malumotlarini saqlashda xatolik yuz berdi.")
        logger.error(f"Failed to save user data: {user_data}")

@router.callback_query(lambda call: call.data == "check_subscription")
async def check_subscription(call: types.CallbackQuery):
    user_id = call.from_user.id
    if await check_user_subscription(user_id):
        buttons = await home_buttons()
        await call.message.edit_text("Xizmatlardan birini tanlang", reply_markup=buttons)
    else:
        buttons = await create_channels_buttons()
        await call.message.edit_text(
            bold("Siz hali hamma kanallarga azo bo'lmadingiz. Iltimos, avval azo bo'ling."),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=buttons
        )
