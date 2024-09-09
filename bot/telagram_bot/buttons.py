from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import aiohttp
from bot.models import User

user=User

async def home_buttons():
    buttons = [
        [InlineKeyboardButton(text="Isimlarga rasmlar 🖼️", callback_data='image_for_name')],
        [InlineKeyboardButton(text="Isimlarga + 🎥", callback_data="video_for_name")],
        [InlineKeyboardButton(text="Nikname lar ✏️", callback_data="nikname")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def group_buttons(buttons, group_size):
    return [buttons[i:i + group_size] for i in range(0, len(buttons), group_size)]


async def create_name_role_buttons():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/api/roles/') as response:
            if response.status == 200:
                roles = await response.json()
                buttons = [InlineKeyboardButton(text=role['name'], callback_data=f'role_{role["id"]}') for role in roles]
                grouped_buttons = group_buttons(buttons, 3)
                return InlineKeyboardMarkup(inline_keyboard=grouped_buttons)
            else:
                raise Exception("Failed to fetch roles")


async def create_image_buttons(role_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://127.0.0.1:8000/api/images/?role_id={role_id}') as response:
            if response.status == 200:
                images = await response.json()
                buttons = [InlineKeyboardButton(text=image['name'], callback_data=f'image_{image["id"]}') for image in images]
                grouped_buttons = group_buttons(buttons, 4)
                return InlineKeyboardMarkup(inline_keyboard=grouped_buttons)
            else:
                raise Exception("Failed to fetch images")
