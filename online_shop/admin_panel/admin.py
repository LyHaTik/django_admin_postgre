from django.contrib import admin
from django.conf import settings
import asyncio
import httpx

from .models import UserTg, Category, SubCategory, Product, CartItem, BroadcastMessage

# Добавить асинхронность и адрес BOT_API_URL
@admin.register(UserTg)
class UserTgAdmin(admin.ModelAdmin):
    list_display = ("id", "phone", "address")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("category", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "subcategory", "price")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order_id", "added_at", "user", "product", "quantity", "is_payed")


@admin.register(BroadcastMessage)
class BroadcastMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "created_at", "sent")
    actions = ["send_broadcast"]

    def send_broadcast(self, request, queryset):
        async def send_all_messages(messages):
            sent_count = 0
            async with httpx.AsyncClient() as client:
                from .models import UserTg
                users = await sync_to_async(list)(UserTg.objects.all())  # конвертируем в async

                for message in messages:
                    if message.sent:
                        continue
                    for user in users:
                        response = await client.post(
                            f"{settings.BOT_API_URL}/send_message/",
                            json={"user_id": user.id, "text": message.text}
                        )
                        if response.status_code == 200:
                            sent_count += 1
                    message.sent = True
                    await sync_to_async(message.save)()
            return sent_count

        # Импорт sync_to_async
        from asgiref.sync import sync_to_async

        messages = list(queryset)
        sent_count = asyncio.run(send_all_messages(messages))

        self.message_user(request, f"Успешно отправлено сообщений: {sent_count}")

    send_broadcast.short_description = "Сделать рассылку"
