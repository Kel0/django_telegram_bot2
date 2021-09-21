import logging
from data.config import BANNED_USERS
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware


class BigBrother(BaseMiddleware):

    async def on_pre_process_update(self, update:types.Update, data: dict):
        logging.info("____________New Update_______________")
        logging.info("Pre Process Update 1")
        logging.info("Next point: Process Update")
        data["middleware_data"] = "this will go till post process update"
        if update.message:
            user = update.message.from_user.id
        elif update.callback_query:
            user = update.callback_query.from_user.id
        else:
            return
        logging.info(f"{BANNED_USERS}")
        logging.info(f"{user}")
        if user in BANNED_USERS:
            raise CancelHandler()

    async def on_process_update(self, update: types.Update, data: dict):
        logging.info("Process Update 2")
        logging.info(f"Next point: Pre Process Message {data=}")

    async def on_pre_process_message(self, update: types.Message, data: dict):
        logging.info("Pre Process Message 3")
        logging.info("Next point: Filter, Process Message")
        data["middleware_data"] = "It will go to process message"
        logging.info(data["middleware_data"])
