from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from .models import Car
from .config import DEFAULT_PER_PAGE


def main_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🗂 Каталог")],
            [KeyboardButton(text="🗑 Корзина")],
        ],
        resize_keyboard=True
    )

def get_phone_request_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Отправить номер", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_paginated_ik(items: list, page: int = 1, per_page: int = DEFAULT_PER_PAGE) -> InlineKeyboardMarkup:
    start = (page - 1) * per_page
    end = start + per_page
    current_items = items[start:end]
    
    item = items[0] if items else None
    
    buttons = []
    
    if isinstance(item, Car):
        for item in current_items:
            buttons.append([InlineKeyboardButton(text="ℹ️ Подробнее", callback_data=f"car_info:{item.id}")])
            buttons.append([InlineKeyboardButton(text="✅ в корзину", callback_data=f"to_cart:{item.id}")])
    else:
        for item in current_items:
            buttons.append([
                InlineKeyboardButton(text=item.name, callback_data=f"item:{item.id}")
            ])

    nav_buttons = []
    if start > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"page:{page-1}"))
    if end < len(items):
        nav_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"page:{page+1}"))

    if nav_buttons:
        buttons.append(nav_buttons)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_edit_count_item_ik(item_id: int, count: int) -> InlineKeyboardMarkup:
    buttons = []

    # ➖/➕ Кнопки количества
    quantity_buttons = []

    # ➖ Кнопка минус (только если count > 1)
    if count > 0:
        quantity_buttons.append(InlineKeyboardButton(
            text="-",
            callback_data=f"minus:{item_id}:{count - 1}"
        ))
    else:
        quantity_buttons.append(InlineKeyboardButton(
            text=" ",
            callback_data="noop"
        ))

    # Число по центру
    quantity_buttons.append(InlineKeyboardButton(
        text=f"{count}",
        callback_data="noop"
    ))

    # ➕ Кнопка плюс
    quantity_buttons.append(InlineKeyboardButton(
        text="+",
        callback_data=f"plus:{item_id}:{count + 1}"
    ))

    buttons.append(quantity_buttons)

    # ✅ Оформить заказ
    buttons.append([
        InlineKeyboardButton(
            text=f"✅ Оформить заказ ({count} шт.)",
            callback_data=f"make_order:"
        )
    ])

    # ↩️ Назад
    buttons.append([
        InlineKeyboardButton(
            text="↩️ Назад",
            callback_data=f"back:"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Переделать, объект модели лучше не передавать
def get_cart_items_ik(cart) -> InlineKeyboardMarkup:
    
    buttons = []

    for item in cart:
        item_name = item.car
        item_car_id = item.car.id
        item_quantity = item.quantity
        buttons.append([
            InlineKeyboardButton(text=f"{item_name}", callback_data="noop"),
            InlineKeyboardButton(text="-", callback_data=f"db_minus:{item_car_id}:{item_quantity - 1}"),
            InlineKeyboardButton(text=f"{item_quantity}", callback_data="noop"),
            InlineKeyboardButton(text="+", callback_data=f"db_plus:{item_car_id}:{item_quantity + 1}"),
            InlineKeyboardButton(text="❌", callback_data=f"db_delete:{item_car_id}")
        ])

    buttons.append([
        InlineKeyboardButton(text="✅ Оплатить", callback_data="db_pay:"),
        InlineKeyboardButton(text="🧹 Очистить", callback_data="db_clean:")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
