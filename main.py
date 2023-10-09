import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, keyboard_button
from aiogram.utils.markdown import hbold
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    reply_keyboard_remove,
)

from handlers import creating_ticket

TOKEN = "6666918790:AAFQtCeV2DVobJ05tpUD_TFkjLkFtydZeKQ"

dp = Dispatcher()


def default_keyboard():
    kb = [[KeyboardButton(text="Тикет")]]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        text=f"Hello, {hbold(message.from_user.full_name)}!",
        reply_markup=default_keyboard(),
    )


async def main() -> None:
    dp.include_routers(creating_ticket.router)
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
