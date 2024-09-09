import logging
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.filters.state import StateFilter
from bot.telagram_bot.tokens import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

# Bot and dispatcher initialization
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()
dp.include_router(router)

# Nickname lists
boy_nicknames = [
    "꧁༺{}༻꧂", "⚔️や{}⚔️", "༺{}༻ᴳᵒᵈ", "▄︻┻═┳一{}",
    "🔥🥀{}🥀🔥", "✰{}✰", "⛓ 💯{}⛓", "⚡{}⚡",
    "۩V͇̿I͇̿P͇̿۩℞{}۩V͇̿I͇̿P͇̿۩", "❍⌇─➭⌗{}: ๑ ˚ ͙۪۪̥◌ ⌨"
]

girl_nicknames = [
    "🌺🌸💮{}💮🌸🌺", "•✗{}💕🐝•", "•✨♡🌼•°{}°•🌼♡✨•",
    "🦋⃟{}✮⃝🇲iss 🇶𝖚𝖊𝖊𝖓𝄟⃝", "😘❤️ {} ꀘ𝗂𝚖𝐛𝙧ᥱ℮❣️💫",
    "🌻{}🌻", "𓆩💜𓆪{}𓆩💜𓆪",
    "¸„.-•~¹°”ˆ˜¨{}¨˜ˆ", "✨💕💖{}💖💕✨",
    "•✨♡🌼•°{}°•🌼♡✨•"
]


# States
class Form(StatesGroup):
    gender_choice = State()
    nickname_choice = State()
    user_name = State()


# Start command handler
@router.message(Command(commands=['start']))
async def cmd_start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Yigit 🙍🏻‍♂️", callback_data="gender_boy"),
         InlineKeyboardButton(text="Qiz 🙍🏻‍♀️", callback_data="gender_girl")]
    ])
    await message.answer("Kim uchun nickname yasash kerak?", reply_markup=keyboard)


# Callback query handler for gender choice
@router.callback_query(lambda c: c.data.startswith('gender_'))
async def process_gender_choice(callback_query: types.CallbackQuery, state: FSMContext):
    gender = callback_query.data.split('_')[1]
    await state.update_data(gender=gender)

    if gender == "boy":
        nicknames = boy_nicknames
    else:
        nicknames = girl_nicknames

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=nickname.format("Ismingiz"), callback_data=f"nick_{i}")]
        for i, nickname in enumerate(nicknames)
    ])

    await callback_query.message.answer("O'zingizga yoqqan nickname ni tanlang:", reply_markup=keyboard)
    await state.set_state(Form.nickname_choice)
    await callback_query.answer()


# Callback query handler for nickname choice
@router.callback_query(lambda c: c.data.startswith('nick_'))
async def process_nickname_choice(callback_query: types.CallbackQuery, state: FSMContext):
    nickname_index = int(callback_query.data.split('_')[1])
    user_data = await state.get_data()
    gender = user_data['gender']
    chosen_nickname = boy_nicknames[nickname_index] if gender == "boy" else girl_nicknames[nickname_index]
    await state.update_data(chosen_nickname=chosen_nickname)
    await callback_query.message.answer("Ismingizni kiriting:")
    await state.set_state(Form.user_name)
    await callback_query.answer()


# Message handler for user name input
@router.message(StateFilter(Form.user_name))
async def process_user_name(message: types.Message, state: FSMContext):
    user_name = message.text
    user_data = await state.get_data()
    chosen_nickname = user_data['chosen_nickname']
    personalized_nickname = chosen_nickname.format(user_name)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Nickname ni ko'chirish", callback_data="copy_nickname")]
    ])

    await message.answer(f"Yangi Nickname ingiz tayyor: {personalized_nickname}", reply_markup=keyboard)
    await state.clear()


# Callback query handler for copying nickname
@router.callback_query(lambda c: c.data == 'copy_nickname')
async def process_copy_nickname(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer("Muvaffaqqiyatli ko'chirildi!", show_alert=True)


# Run the bot
if __name__ == '__main__':
    dp.run_polling(bot)
