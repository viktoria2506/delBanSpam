import random
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, ContentType, KeyboardButton
from config import Config, load_config
config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token

API_TOKEN = '6707863597:AAHZdZk0HlDLIIeWBZ6rbwAJ5cVgbN2-LFc'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Этот хэндлер будет срабатывать на команду "/start"
@dp.message_handler(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\n\n'
                         'Это бот для очистки спам сообщений в вашем канале')


bad_words = ['фальш рубл', 'фальшивые рубли', 'фальш деньг', 'фальшивые деньги', 'фальшивые купюры', 'фальш купю',
             'голые фот',
             'казино', '1weawx', 'букмекер', '1win', 'casino',
             'поддельные рубли', 'поддельные деньги', 'поддельные купюры',
             'интим фото']

# функция для проверки наличия запрещенных слов в сообщении
def check_message(message):
    for word in bad_words:
        if word in message.text.lower():
            return True
    return False

# Этот хэндлер будет срабатывать на остальные текстовые сообщения
@dp.message_handler()
async def process_text_answers(message: Message):
    print(message)
    if check_message(message):
        print("spam")
        await bot.delete_message(message.chat.id, message.message_id)
    else:
        print("ok")

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
asyncio.run(dp.start_polling(bot))

# if __name__ == '__main__':
#    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#    asyncio.run(dp.start_polling(bot))

