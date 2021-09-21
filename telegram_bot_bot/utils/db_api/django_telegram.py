from asgiref.sync import sync_to_async
from django_telegram.client.models import Client


@sync_to_async
def save_client(data):
    if not Client.objects.filter(telegram_id=data["telegram_id"]).first():
        Client.objects.create(
            name=data["name"],
            surname=data["surname"],
            telegram_id=data["telegram_id"],
            bin=data["BIN"],
            address=data["address"],
        )
