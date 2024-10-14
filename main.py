import random
import asyncio
import logging
import sys
import re
from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, ContentType, KeyboardButton
from config import Config, load_config
from constants import bad_words, replacements

config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Этот хэндлер будет срабатывать на команду "/start"
@dp.message_handler(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\n\n'
                         'Это бот для очистки спам сообщений в вашем канале')


def preprocess_message(message):
    # Заменяем каждый символ в сообщении
    for original, pattern in replacements.items():
        message = re.sub(pattern, original, message, flags=re.IGNORECASE)

    return message

def check_message(message):
    message_lower = message.text.lower()

    processed_message = preprocess_message(message_lower)

    # Использование регулярных выражений для поиска слов
    for word in bad_words:
        pattern = r'\b' + re.escape(word)
        if re.search(pattern, processed_message):
            return True
    return False

@dp.message_handler()
async def process_text_answers(message: Message):
    if check_message(message):
        await bot.delete_message(message.chat.id, message.message_id)
        try:
            await bot.ban_chat_member(message.chat.id, message.from_user.id)
        except Exception as e:
           print("Не удалось заблокировать пользователя: {e}")

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
asyncio.run(dp.start_polling(bot))

# if __name__ == '__main__':
#    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#    asyncio.run(dp.start_polling(bot))

