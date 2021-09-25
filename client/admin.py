from django.contrib import admin
from .models import Client, Franchise, BalanceHistory, SalePoint, FAQ, SpecialOffer, Role, ClientRequest


@admin.register(ClientRequest)
class ClientRequest(admin.ModelAdmin):
    list_display = ("id", "request_type", "status", "request_info", "comment")
    readonly_fields = ("request_info", "telegram_id")
    list_filter = ("request_type", "status")


@admin.register(Franchise)
class FranсhiseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "balance")


@admin.register(BalanceHistory)
class BalanceHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "franchise", "amount", "date", "type",)
    list_filter = ("type",)
    raw_id_fields = ("franchise",)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "surname", "address", "telegram_id", "franchise")
    raw_id_fields = ("franchise",)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("id", "role")


@admin.register(SalePoint)
class SalePointAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "link",)


@admin.register(SpecialOffer)
class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "answer",)


