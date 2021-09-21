from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField
from django.dispatch import receiver
from django.db.models.signals import post_save
import requests, json
from telegram_bot_bot.data import config


class Franсhise(models.Model):
    name = models.CharField(max_length=1024)
    balance = models.IntegerField(null=True, blank=True, default=0)
    bin = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Role(models.Model):
    role = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.role}"


class Client(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    telegram_id = models.IntegerField(null=True, blank=True, default=-1)
    address = models.CharField(max_length=255, null=True, blank=True)
    royalty = models.IntegerField(null=True, blank=True, default=50)
    royalty_expires = models.DateField(null=True, blank=True)
    franchise = models.ForeignKey(Franсhise, on_delete=models.CASCADE, null=True, blank=True, related_name="franchise")
    requisites = models.CharField(max_length=512, default=0)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    info = JSONField(blank=True, null=True, editable=False)
    def __str__(self):
        return f"{self.name} {self.surname}"


class SpecialOffer(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


CHOICES = (
        ('up', 'Пополнение'),
        ('down', 'Списание'),
    )


class BalanceHistory(models.Model):
    amount = models.IntegerField(null=True, blank=True, default=0)
    franchise = models.ForeignKey(Franсhise, on_delete=models.CASCADE, null=True, blank=True, related_name="franchisee")
    date = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=64, choices=CHOICES)


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=1024)


class SalePointType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SalePoint(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(SalePointType, on_delete=models.CASCADE, null=True, blank=True, related_name="type")
    link = models.CharField(max_length=512, blank=True, null=True)

    def __str__(self):
        return self.name


REQUEST_TYPES = (
        ('registration', 'Регистрация'),
        ('top_up_balance', 'Пополнение баланса')
    )
STATUS_TYPES = (
        ('accepted', 'Принято'),
        ('declined', 'Отказано'),
        ('processing', 'В рассмотрении')
    )


class ClientRequest(models.Model):
    request_type = models.CharField(choices=REQUEST_TYPES, max_length=255)
    status = models.CharField(choices=STATUS_TYPES, max_length=25, default='processing')
    comment = models.TextField(null=True, blank=True)
    request_info = models.TextField(null=True, blank=True)
    info = JSONField(blank=True, null=True, editable=False)
    date = models.DateField(auto_now_add=True)
    telegram_id = models.IntegerField(null=True, blank=True)


@receiver(post_save, sender=ClientRequest)
def client_request_signal(sender, instance, **kwargs):
    if instance.status == "processing":
        return
    elif instance.status == "declined":
        text = "Отказано\n"
        text += instance.comment
    else:
        data = json.loads(instance.info)
        if instance.request_type == "registration":
            role = Role.objects.get(role=data["role"])
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
                    info=json.dumps(data),
                )
            text = "Одобрено\n"
            text += instance.comment
        elif instance.request_type == "top_up_balance":
            amount = data["balance_amount"]
            cl = Client.objects.filter(telegram_id=data["telegram_id"]).first()
            franchise = cl.franchise
            franchise.balance += amount
            franchise.save()
            BalanceHistory.objects.create(franchise=franchise, amount=amount, type="up")
            text = f"Баланс пополнен на {amount}\n"
            text += instance.comment
    requests.get(
        f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage?chat_id={instance.telegram_id}&text={text}")
