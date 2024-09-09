from bot.telagram_bot.tokens import BOT_TOKEN
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

API_TOKEN = BOT_TOKEN
DJANGO_API_URL = 'http://127.0.0.1:8000/api/video/'
ORDER_API_URL = 'http://127.0.0.1:8000/api/ordervideo/'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer("Salom! Video qidirish uchun /search buyrug'ini bering.")

@dp.message(Command("search"))
async def search_videos(message: types.Message):
    await message.answer("Iltimos, video nomini kiriting:")

@dp.message()
async def handle_video_search(message: types.Message):
    query = message.text
    response = requests.get(DJANGO_API_URL)
    if response.status_code == 200:
        videos = response.json().get('videos', [])
        matching_videos = [video for video in videos if query.lower() in video['name'].lower()]
        if matching_videos:
            await display_videos(message, matching_videos, page_num=1)
        else:
            await handle_no_results(message)
    else:
        await message.answer("Videolar ro'yxatini olishda xatolik yuz berdi.")

async def display_videos(message: types.Message, videos, page_num: int):
    page_size = 10
    start_idx = (page_num - 1) * page_size
    end_idx = start_idx + page_size
    page_videos = videos[start_idx:end_idx]
    total_videos = len(videos)
    
    if not page_videos:
        await message.answer("Sahifa mavjud emas.")
        return
    
    video_list = "\n".join([f"{start_idx + idx + 1}. {video['name']}" for idx, video in enumerate(page_videos)])
    
    inline_keyboard = []
    
    for idx, video in enumerate(page_videos):
        inline_keyboard.append([InlineKeyboardButton(text=str(start_idx + idx + 1), callback_data=f"video_{video['id']}")])
    
    if total_videos > page_size:
        navigation_buttons = []
        if page_num > 1:
            navigation_buttons.append(InlineKeyboardButton(text="Orqaga", callback_data=f"pagination_prev_{page_num-1}"))
        if end_idx < total_videos:
            navigation_buttons.append(InlineKeyboardButton(text="Oldinga", callback_data=f"pagination_next_{page_num+1}"))
        if navigation_buttons:
            inline_keyboard.append(navigation_buttons)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    
    await message.answer(f"Qidiruv natijalari:\n{video_list}", reply_markup=keyboard)

async def handle_no_results(message: types.Message):
    order_response = requests.get(ORDER_API_URL)
    if order_response.status_code == 200:
        order_videos = order_response.json()
        if isinstance(order_videos, list) and order_videos:
            order_video = order_videos[0]
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Buyurtma qilish", url=order_video['url'])]
            ])
            await message.answer("Hech qanday mos video topilmadi. Buyurtma qilish uchun quyidagi tugmani bosing:", reply_markup=keyboard)
        else:
            await message.answer("Buyurtma uchun kanal yoki guruh topilmadi brat.")
    else:
        await message.answer("Buyurtma ma'lumotlarini olishda xatolik yuz berdi.")

@dp.callback_query(lambda c: c.data.startswith("video_"))
async def send_video(callback_query: types.CallbackQuery):
    video_id = callback_query.data.split("_")[1]
    video_url = f"{DJANGO_API_URL}{video_id}/"
    video_response = requests.get(video_url)
    if video_response.status_code == 200:
        video_data = video_response.json()
        video_file_url = video_data['video']
        if video_file_url:
            await bot.send_video(callback_query.from_user.id, video=video_file_url)
        else:
            await callback_query.answer("Video URL manzili topilmadi.")
    else:
        await callback_query.answer("Videoni olishda xatolik yuz berdi.")

@dp.callback_query(lambda c: c.data.startswith("pagination_"))
async def paginate_videos(callback_query: types.CallbackQuery):
    action, page_num = callback_query.data.split("_")[1:]
    page_num = int(page_num)
    
    if action == "prev":
        page_num -= 1
    elif action == "next":
        page_num += 1
    
    query = callback_query.message.reply_to_message.text.split(":", 1)[1].strip()
    response = requests.get(DJANGO_API_URL)
    if response.status_code == 200:
        videos = response.json().get('videos', [])
        matching_videos = [video for video in videos if query.lower() in video['name'].lower()]
        if matching_videos:
            await display_videos(callback_query.message.reply_to_message, matching_videos, page_num)
    await callback_query.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
