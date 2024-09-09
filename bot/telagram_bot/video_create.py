import logging
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from bot.telagram_bot.tokens import BOT_TOKEN
from aiogram.exceptions import TelegramBadRequest

API_TOKEN = BOT_TOKEN
DJANGO_API_URL = 'http://127.0.0.1:8000/api/video/'
ORDER_API_URL = 'http://127.0.0.1:8000/api/ordervideo/'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

logging.basicConfig(level=logging.INFO)

class UploadVideo(StatesGroup):
    waiting_for_video = State()
    waiting_for_name = State()

@dp.message(Command("start"))
async def send_welcome(message: types.Message, state: FSMContext):
    await message.answer("Video yuboring:")
    await state.set_state(UploadVideo.waiting_for_video)

@dp.message(UploadVideo.waiting_for_video, F.content_type == types.ContentType.VIDEO)
async def process_video(message: types.Message, state: FSMContext):
    video = message.video
    await state.update_data(video=video)
    await message.answer("Videoga nom bering:")
    await state.set_state(UploadVideo.waiting_for_name)

@dp.message(UploadVideo.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    data = await state.get_data()
    video = data['video']
    
    try:
        # Fayl ma'lumotlarini olish va yuklab olish
        file_info = await bot.get_file(video.file_id)
        file_path = file_info.file_path
        logging.info(f"Fayl yo'li: {file_path}")  # Fayl yo'lini loglash
        video_file = await bot.download(file_path)
        logging.info(f"Video fayl yuklandi: {video_file}")  # Fayl yuklangani haqida log

        # Django ga video saqlash
        files = {'video': (video.file_name, video_file)}
        data = {'name': name}
        response = requests.post(DJANGO_API_URL, data=data, files=files)
        
        if response.status_code == 201:
            await message.answer("Video saqlandi.")
            
            # OrderVideo modelidan kanal ID olish
            response = requests.get(ORDER_API_URL)
            if response.status_code == 200:
                order_videos = response.json()
                if order_videos:
                    channel_id = order_videos[0]['channel_id']
                    
                    # Kanalga video yuborish
                    await bot.send_video(chat_id=channel_id, video=video.file_id, caption=name)
                    await message.answer("Video kanalga yuborildi.")
                else:
                    await message.answer("Kanal ma'lumotlari topilmadi.")
            else:
                await message.answer("Kanal ma'lumotlarini olishda xatolik.")
        else:
            await message.answer("Videoni saqlashda xatolik.")
    except TelegramBadRequest as e:
        await message.answer(f"Telegramdan xatolik: {e}")
    except Exception as e:
        await message.answer(f"Xatolik: {e}")
    
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

