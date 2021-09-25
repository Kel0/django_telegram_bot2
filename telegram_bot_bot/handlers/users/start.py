from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from filters.private_chat import IsPrivate
from loader import dp
import logging
from states.test import Test
from utils.misc import rate_limit
from telegram_bot_bot.keyboards.inline.buttons import register_query
from client.models import Client
from client.utils import get_client
from telegram_bot_bot.keyboards.inline.buttons import owner_keyboard, register_keyboard, technical_specialist_keyboard, \
    manager_keyboard


@rate_limit(15, key="start")
@dp.message_handler(CommandStart(), IsPrivate())
async def bot_start(message: types.Message):
    await show_keyboard(message)


async def show_keyboard(message):
    data = await get_client(message.chat.id)
    if "registered" in data:
        await message.answer(f"Добрый день! Вам нужно заполнить анкету", reply_markup=register_keyboard)
    elif "processing" in data:
        await message.answer(f"Заявка в обработке")
    elif data["role"] == "owner":
        await message.answer(f"Здравствуйте {data['surname']} {data['name']}.", reply_markup=owner_keyboard)
    elif data["role"] == "technical":
        await message.answer(f"Здравствуйте {data['surname']} {data['name']}.",
                             reply_markup=technical_specialist_keyboard)
    else:
        await message.answer(f"Здравствуйте {data['surname']} {data['name']}.",
                             reply_markup=manager_keyboard)