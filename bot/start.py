
from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()


@router.message(CommandStart())
async def start_(message: types.Message):
    await message.answer("Salom Dunyo")
