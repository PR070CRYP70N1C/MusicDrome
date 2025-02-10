import asyncio
from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter
from logger import logger

async def send_worker(bot: Bot, message_queue: asyncio.Queue):
    while True:
        chat_id, text, reply_to_id = await message_queue.get()
        try:
            success = False
            while not success:
                try:
                    await bot.send_message(chat_id=chat_id, text=text, reply_to_message_id=reply_to_id)
                    success = True
                except TelegramRetryAfter as e:
                    logger.warning(f"Flood control: ждем {e.retry_after} сек.")
                    await asyncio.sleep(e.retry_after)
                except Exception as exc:
                    logger.error(f"Ошибка при отправке сообщения: {exc}")
                    success = True
            await asyncio.sleep(0.5)
        finally:
            message_queue.task_done()

async def add_task_to_queue(message_queue: asyncio.Queue, bot: Bot, chat_id: int, text: str, reply_to_id: int):
    await message_queue.put((chat_id, text, reply_to_id))
