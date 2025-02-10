import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from config import API_TOKEN, LOCAL_TELEGRAM_SERVER
from worker import send_worker
from handlers import handle_audio

def create_bot():
    session = AiohttpSession(api=TelegramAPIServer.from_base(LOCAL_TELEGRAM_SERVER, is_local=True))
    return Bot(token=API_TOKEN, session=session)

async def main():
    message_queue = asyncio.Queue()
    bot = create_bot()
    dp = Dispatcher()

    asyncio.create_task(send_worker(bot, message_queue))

    @dp.message(F.audio)
    async def handle_audio_wrapper(message: Message):
        await handle_audio(message, message_queue)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
