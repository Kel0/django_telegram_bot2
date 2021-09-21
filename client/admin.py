from django.contrib import admin
from .models import Client, Franсhise, BalanceHistory, SalePointType, SalePoint, FAQ, SpecialOffer, Role, ClientRequest


@admin.register(ClientRequest)
class ClientRequest(admin.ModelAdmin):
    list_display = ("id", "request_type", "status", "request_info", "comment")
    readonly_fields = ("request_info", "telegram_id")
    list_filter = ("request_type", "status")


@admin.register(Franсhise)
class FranсhiseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "balance", "bin")


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
    list_display = ("id", "name", "type", "link")
    raw_id_fields = ("type",)
    list_filter = ("type",)


@admin.register(SalePointType)
class SalePointTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(SpecialOffer)
class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "answer",)


