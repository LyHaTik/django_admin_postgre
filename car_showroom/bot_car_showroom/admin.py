from django.contrib import admin
import asyncio

from .models import User, CarCategory, CarBrand, Car, Cart
from .services import broadcast_message
from .config import NEWSLETTER_TEXT


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "phone", "address", "is_staff")
    actions = ["send_broadcast"]

    def send_broadcast(self, request, queryset):
        user_ids = list(queryset.values_list("id", flat=True))
        text = NEWSLETTER_TEXT
        asyncio.run(broadcast_message(text, user_ids))
        self.message_user(request, f"Сообщение отправлено {len(user_ids)} пользователям")

    send_broadcast.short_description = "🔔 Сделать рассылку"


@admin.register(CarCategory)
class CarCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("brand", "model_name", "category", "price", "year", "mileage")
    list_filter = ("brand", "category", "year")
    search_fields = ("model_name", "description")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "car", "quantity", "added_at")
    list_filter = ("user", "added_at")
