from django.contrib import admin
from asgiref.sync import async_to_sync

from .models import User, Product, MailingMessage, Category, SubCategory, Cart
from .services import broadcast_message
from .db import mailing_text


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "phone", "address", "is_staff")
    actions = ["send_broadcast"]

    def send_broadcast(self, request, queryset):
        user_ids = list(queryset.values_list("id", flat=True))
        text = async_to_sync(mailing_text)()
        if text:
            async_to_sync(broadcast_message)(text, user_ids)
            self.message_user(request, f"Сообщение отправлено {len(user_ids)} пользователям")
        else:
            self.message_user(request, f"Нет сообщений для отправки!")

    send_broadcast.short_description = "🔔 Сделать рассылку"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "added_at", "order_id", "user", "product", "quantity", "is_payed")
    search_fields = ("user", "order_id", "product",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "subcategory", "price", "description")
    list_filter = ("subcategory",)
    search_fields = ("name", "subcategory")


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    list_display = ("text", "is_sent")
