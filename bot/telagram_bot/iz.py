from bot.telagram_bot.tokens import BOT_TOKEN
API_TOKEN = BOT_TOKEN
API_URL = 'http://127.0.0.1:8000/api/mandatory-users/'
import logging
import requests
from aiogram import Bot, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

def fetch_channels():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()  # Assuming your API returns a JSON response with channel details
    else:
        logging.error(f"Failed to fetch channels: {response.status_code}")
        return []

@router.message(Command('start'))
async def send_welcome(message: Message):
    channels = fetch_channels()
    buttons = [
        InlineKeyboardButton(text=channel['name'], url=f"https://t.me/{channel['url']}")
        for channel in channels
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])
    await message.answer("Please join all the channels below:", reply_markup=keyboard)
    await message.answer("After joining all channels, send /check_channels to verify your membership status.")

async def check_membership(user_id: int, channel_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logging.error(f"Error checking membership for channel_id {channel_id}: {e}")
        return False

@router.message(Command('check_channels'))
async def check_channels(message: Message):
    user_id = message.from_user.id
    channels = fetch_channels()

    all_members = True
    for channel in channels:
        is_member = await check_membership(user_id, channel['channel_id'])
        if not is_member:
            all_members = False
            await message.answer(f"You are not a member of {channel['name']}. Please join the channel.")
    
    if all_members:
        await message.answer("Welcome! You are a member of all the channels.")

dp.include_router(router)

if __name__ == '__main__':
    dp.run_polling(bot)
