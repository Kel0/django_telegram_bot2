from loader import dp, bot
from aiogram import types
from aiogram.dispatcher.filters import Command
from states.test import Test
from aiogram.dispatcher.storage import FSMContext
from client.utils import (save_client, current_balance, get_faq, get_special_offer, top_up_balance_method,
                          balance_history_method, request_register, request_to_manager, get_client, get_franchise,
                          get_special_offers, request_to_promotion)
from telegram_bot_bot.data.config import ADMINS
from telegram_bot_bot.keyboards.inline.buttons import (yes_no_keyboard, balance_keyboard, sale_point_keyboard,
                                                       promotion_keyboard)
from .start import show_keyboard


@dp.callback_query_handler(lambda c: c.data == "balance")
async def balance_menu(call):
    await call.answer(cache_time=60)
    await call.message.answer("Операции с балансом", reply_markup=balance_keyboard)


@dp.callback_query_handler(lambda c: c.data == "balance_history_query")
async def balance_history(call):
    await call.answer(cache_time=60)
    await call.message.answer("Введите количество последних операции")
    await Test.balance_history_count.set()


@dp.message_handler(state=Test.balance_history_count)
async def balance_history_send(message: types.Message, state: FSMContext):
    try:
        m = int(message.text)
    except:
        await message.answer("Введите число")
        return
    f = await balance_history_method(m, message.chat.id)
    await bot.send_document(message.chat.id, open(f"{message.chat.id}.xlsx", "rb"))
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == "top_up_balance_query")
async def top_up_balance(call):
    await call.answer(cache_time=60)
    await call.message.answer("Пополнение баланса, напишите сумму для пополнения")
    await Test.balance_amount.set()


@dp.message_handler(state=Test.balance_amount)
async def balance_amount(message: types.Message, state: FSMContext):
    answer = message.text
    try:
        answer = int(answer)
    except:
        await message.answer("Введите число")
        return
    await state.update_data({"balance_amount": answer})
    # async with state.proxy() as data:
    #     data["answer1"] = answer

    await message.answer("Внесите чек об оплате")
    await Test.payment_reciept.set()


@dp.message_handler(state=Test.payment_reciept, content_types=types.ContentTypes.ANY)
async def balance_reciept(message: types.Message, state: FSMContext):
    answer = message.document
    if not answer:
        await message.answer("Внесите чек об оплате")
    else:
        await state.update_data({"file_id": answer["file_id"]})
        # async with state.proxy() as data:
        #     data["answer1"] = answer

        await message.answer("Напишите ПОДТВЕРЖДАЮ")
        await Test.Q7.set()


@dp.callback_query_handler(lambda c: c.data == "balance_query")
async def balance(call):
    await call.answer(cache_time=60)
    bal = await current_balance(call.message.chat.id)
    await call.message.answer(f"Текущий баланс равен {bal}")


@dp.callback_query_handler(lambda c: c.data == "sale_point")
async def sale_point_menu(call):
    await call.answer(cache_time=60)
    await call.message.answer("Операции с тороговой точкой", reply_markup=sale_point_keyboard)


@dp.callback_query_handler(lambda c: c.data == "sale_point_query")
async def sale_point(call):
    await call.answer(cache_time=60)
    await call.message.answer("Вопросы ответы")


@dp.callback_query_handler(lambda c: c.data == "sale_point_activation_query")
async def sale_point_activation(call):
    await call.answer(cache_time=60)
    await call.message.answer("Вопросы ответы")


@dp.callback_query_handler(lambda c: c.data == "promotion")
async def promotion_menu(call):
    await call.answer(cache_time=60)
    await call.message.answer("Операции с акциями", reply_markup=promotion_keyboard)


@dp.callback_query_handler(lambda c: c.data == "promotion_terms_query")
async def promotion_terms(call):
    await call.answer(cache_time=60)
    mes = await get_special_offer()
    await call.message.answer(mes)


@dp.callback_query_handler(lambda c: c.data == "promotion_apply_query")
async def promotion_apply(call):
    await call.answer(cache_time=60)
    special_offers_keybord = types.InlineKeyboardMarkup()
    spes = await get_special_offers()
    for i in spes:
        r = types.InlineKeyboardButton(i, callback_data="special_offers_keybord" + i)
        special_offers_keybord.row(r)
    await call.message.answer("Выберите акцию", reply_markup=special_offers_keybord)


@dp.callback_query_handler(lambda c: "special_offers_keybord" in c.data)
async def promotion_apply_handle(call):
    await call.answer(cache_time=60)
    data = await get_client(call.message.chat.id)
    data["promotion"] = call.data[22:]
    await request_to_promotion(data)
    await call.message.answer("Ожидайте ответа")


@dp.callback_query_handler(lambda c: c.data == "promotion_suggestion_query")
async def promotion_suggestion(call):
    await call.answer(cache_time=60)
    await call.message.answer("Вопросы ответы")


@dp.callback_query_handler(lambda c: c.data == "feedback_query")
async def feedback_query(call):
    await call.answer(cache_time=60)
    mes = await get_faq()
    await call.message.answer(mes)


@dp.callback_query_handler(lambda c: c.data == "payment_query")
async def payment(call):
    await call.answer(cache_time=60)
    reqs = await get_client(call.message.chat.id)
    await call.message.answer(f"Ваши реквизиты {reqs['requisites']}\n На какую сумму выставить счет ?")
    await Test.payment.set()


@dp.message_handler(state=Test.payment)
async def payment_get(message: types.Message, state: FSMContext):
    answer = message.text
    try:
        answer = int(answer)
    except:
        await message.answer("Напишите число")
        return
    data = await get_client(message.chat.id)
    data["balance_amount"] = answer
    await request_to_manager(data, "payment")
    await message.answer("Заявка в обработке")
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == "faq_query")
async def faq(call):
    await call.answer(cache_time=60)
    mes = await get_faq()
    await call.message.answer(mes)


@dp.callback_query_handler(lambda c: c.data == "register_query")
async def register(call):
    await call.answer(cache_time=60)
    await call.message.answer("Напишите свое имя")
    await Test.Q1.set()


@dp.message_handler(state=Test.Q1)
async def register_name(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data({"name": answer})

    # async with state.proxy() as data:
    #     data["answer1"] = answer

    await message.answer("Напишите свою фамилию")
    await Test.Q2.set()


@dp.message_handler(state=Test.Q2)
async def register_surname(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data({"surname": answer})

    # async with state.proxy() as data:
    #     data["answer1"] = answer

    await message.answer("Напишите свой БИН")
    await Test.Q3.set()


@dp.message_handler(state=Test.Q3)
async def register_bin(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data({"bin": answer})

    # async with state.proxy() as data:
    #     data["answer1"] = answer
    if "balance" in await state.get_data():
        await message.answer("Напишите сумму пополнения")
        await Test.balance_amount.set()
    else:
        await message.answer("Напишите свой юр адресс")
        await Test.Q4.set()


@dp.message_handler(state=Test.Q4)
async def register_address(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data({"address": answer})
    await message.answer("Какая ваша должность:\n"
                         "Напиши 1 если владелец\n"
                         "Напиши 2 если аккаунт менеджер\n"
                         "Напиши 3 если тех.специалист\n"
                         )
    await Test.Q5.set()
    # async with state.proxy() as data:
    #     data["answer2"] = answer


@dp.message_handler(state=Test.Q5)
async def register_role(message: types.Message, state: FSMContext):
    answer = message.text
    mes = "Какая ваша должность:\n"\
          "Напиши 1 если владелец\n"\
          "Напиши 2 если аккаунт менеджер\n"\
          "Напиши 3 если тех.специалист\n"
    try:
        answer = int(answer)
        if answer in [1, 2, 3]:
            pos = {1: "owner",
                   2: "manager",
                   3: "technical"}
            await state.update_data({"role": pos[answer]})
            franchise_list = await get_franchise()
            mess = ""
            for f in franchise_list:
                mess = mess + f + "\n"
            await message.answer("Напишите имя франшизы\n" + "Варианты:\n" + mess)
            await state.update_data({"franchise_list": franchise_list})
            await Test.Q6.set()
        else:
            print(2)
            await message.answer(mes)
    except:
        print(3)
        await message.answer(mes)


@dp.message_handler(state=Test.Q6)
async def register_franchise(message: types.Message, state: FSMContext):
    answer = message.text
    data = await state.get_data()
    franchise_list = data["franchise_list"]
    if answer not in franchise_list:
        mess = ""
        for f in franchise_list:
            mess = mess + f + "\n"
        await message.answer("Напишите имя франшизы\n" + "Варианты:\n" + mess)
    else:
        await state.update_data({"franchise": answer})
        await message.answer("Напишите свои реквизиты")
        await Test.Q7.set()


@dp.message_handler(state=Test.Q7)
async def register_requisites(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data({"requisites": answer})
    await state.update_data({"telegram_id": message.chat.id})
    data = await state.get_data()

    if "balance_amount" in data and answer == "ПОДТВЕРЖДАЮ":
        client_data = await get_client(message.chat.id)
        client_data["balance_amount"] = data["balance_amount"]
        client_data["telegram_id"] = message.chat.id
        client_data["file_id"] = data["file_id"]
        mess = "Анкета создана успешно\n" \
               f"Имя: {client_data['name']}\n" \
               f"Фамилия: {client_data['surname']}\n" \
               f"БИН: {client_data['bin']}\n" \
               f"Франшиза: {client_data['franchise']}\n" \
               f"Реквизиты: {client_data['requisites']}\n" \
               f"Сумма: {client_data['balance_amount']}\n" \

        await message.answer("Ожидайте ответа")
        await bot.send_document(int(ADMINS[0]), client_data["file_id"])
        await request_to_manager(client_data, "top_up_balance")
    elif "balance_amount" in data:
        await state.finish()
        await show_keyboard(message)
        mess = "Совершена отмена"
    else:
        mess = "Анкета создана успешно\n" \
               f"Имя: {data['name']}\n" \
               f"Фамилия: {data['surname']}\n" \
               f"БИН: {data['bin']}\n" \
               f"Франшиза: {data['franchise']}\n" \
               f"Реквизиты: {data['requisites']}\n" \
               f"Адрес: {data['address']}\n" \
               f"Должность: {data['role']}\n" \

        await message.answer("Анкета создана! Ожидайте ответа")
        data.pop('franchise_list')
        await request_register(data)
    await bot.send_message(chat_id=int(ADMINS[0]), text=mess)
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == "exit", state="*")
async def exit(call, state: FSMContext):
    await call.answer(cache_time=60)
    await state.finish()
    await show_keyboard(call.message)


@dp.callback_query_handler(lambda c: True, state="*")
async def exception(call, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.answer(f"Подождите")
    await state.finish()
