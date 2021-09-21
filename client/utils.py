from asgiref.sync import sync_to_async
from .models import Client, FAQ, SpecialOffer, Franсhise, Role, BalanceHistory, ClientRequest
import requests
import csv
import datetime
import json
import xlsxwriter
from pyexcel.cookbook import merge_all_to_a_book
# import pyexcel.ext.xlsx # no longer required if you use pyexcel >= 0.2.2
import glob


@sync_to_async
def request_register(data):
    mes = f"Имя: {data['name']}\n" \
          f"Фамилия: {data['surname']}\n" \
          f"БИН: {data['bin']}\n" \
          f"Франшиза: {data['franchise']}\n" \
          f"Реквизиты: {data['requisites']}\n" \
          f"Адрес: {data['address']}\n" \
          f"Должность: {data['role']}\n"
    ClientRequest.objects.create(
        request_type="registration", request_info=mes,
        info=json.dumps(data), telegram_id=data["telegram_id"]
    )


@sync_to_async
def request_top_up_balance(data):
    mess = f"Имя: {data['name']}\n" \
           f"Фамилия: {data['surname']}\n" \
           f"БИН: {data['bin']}\n" \
           f"Франшиза: {data['franchise']}\n" \
           f"Реквизиты: {data['requisites']}\n" \
           f"Сумма: {data['balance_amount']}\n"
    ClientRequest.objects.create(
        request_type="top_up_balance", request_info=mess,
        info=json.dumps(data), telegram_id=data["telegram_id"]
    )


@sync_to_async
def get_faq():
    faqs = FAQ.objects.all()
    mes = ""
    for f in faqs:
        mes = mes + f.question + '\n'
        mes = mes + f.answer + '\n'

    return mes


@sync_to_async
def get_special_offer():
    spes = SpecialOffer.objects.all()
    mes = ""
    for s in spes:
        mes = mes + s.name + '\n'
        mes = mes + s.description + '\n'
    return mes


@sync_to_async
def get_client(telegram_id):
    if not ClientRequest.objects.filter(telegram_id=telegram_id).first():
        return {"registered": False}
    cl = Client.objects.filter(telegram_id=telegram_id).first()
    if not cl:
        return {"processing": True}
    return json.loads(cl.info)


@sync_to_async
def top_up_balance_method(telegram_id, amount):
    cl = Client.objects.filter(telegram_id=telegram_id).first()
    if not cl:
        return False
    franchise = cl.franchise
    franchise.balance += amount
    franchise.save()
    BalanceHistory.objects.create(franchise=franchise, amount=amount, type="up")
    return f"Баланс пополнен на {amount}"


@sync_to_async
def save_client(data):
    # r = requests.get(f'https://antcall.bitrix24.ru/rest/1/st30venc8oq24nrt/crm.lead.add.json?FIELDS[TITLE]=Новый лид&FIELDS[NAME]={data["name"]}&FIELDS[LAST_NAME]={data["surname"]}&FIELDS[SCHET]=0&FIELDS[BIN]={data["BIN"]}&FIELDS[POSITION]=worker')
    role = Role.objects.get_or_create(role=data["role"])[0]
    franchise = Franсhise.objects.get_or_create(name=data["franchise"], bin=data["bin"])[0]
    if not Client.objects.filter(telegram_id=data["telegram_id"]).first():
        Client.objects.create(
            name=data["name"],
            surname=data["surname"],
            telegram_id=data["telegram_id"],
            address=data["address"],
            franchise=franchise,
            role=role,
            requisites=data["requisites"],
        )
    return "Вы успешно добавлены"


@sync_to_async
def current_balance(id):
    c = Client.objects.filter(telegram_id=int(id)).first()
    import logging
    if not c:
        return -1
    return c.franchise.balance


@sync_to_async
def balance_history_method(number, telegram_id):
    cl = Client.objects.filter(telegram_id=telegram_id).first()
    bal = BalanceHistory.objects.filter(franchise=cl.franchise).order_by("-date")[:number]
    workbook = xlsxwriter.Workbook(f'{telegram_id}.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Тип операции')
    worksheet.write('B1', 'Дата')
    worksheet.write('C1', 'Сумма')
    r = 2
    for b in bal:
        csvstr = datetime.datetime.strftime(b.date, '%d/%m/%Y')
        worksheet.write(f'A{r}', b.type)
        worksheet.write(f'B{r}', csvstr)
        worksheet.write(f'C{r}', b.amount)
        r += 1
    workbook.close()
