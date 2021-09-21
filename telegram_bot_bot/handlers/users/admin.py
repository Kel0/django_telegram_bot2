from filters import IsPrivate
from loader import dp
from data.config import ADMINS
from aiogram import types


@dp.message_handler(IsPrivate(),user_id=ADMINS, text="secret")
async def admin_chat_secret(message: types.Message):
    await message.answer("It is private message invoked by admin in private chat")
