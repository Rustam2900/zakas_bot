import aiohttp
import logging
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.telagram_bot.tokens import API_URL,BOT_TOKEN
from aiogram import Bot
import requests

bot=Bot(BOT_TOKEN)
async def get_mandatory_channels():
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as response:
            if response.status == 200:
                return await response.json()
            return []

async def create_channels_buttons():
    channels = await get_mandatory_channels()
    buttons = [
        [InlineKeyboardButton(text=channel['name'], url=channel['url']) for channel in channels],
        [InlineKeyboardButton(text="Azolikni tekshirish ✔️", callback_data="check_subscription")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def check_user_subscription(user_id):
    channels = fetch_channels()

    for channel in channels:
        is_member = await check_membership(user_id, channel['channel_id'])
        if not is_member:
            return False
    return True

def fetch_channels():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Failed to fetch channels: {response.status_code}")
        return []

async def check_membership(user_id: int, channel_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logging.error(f"Error checking membership for channel_id {channel_id}: {e}")
        return False
