from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import DEFAULT_PER_PAGE


async def paginated_ik(items: list, page: int=1, per_page=DEFAULT_PER_PAGE) -> InlineKeyboardMarkup:
    start = (page - 1) * per_page
    end = start + per_page
    
    current_items = items[start:end]
    
    buttons = []
    for item in current_items:
        buttons.append([InlineKeyboardButton(text=f"✅ {item['name']}", callback_data=f"item:{item['id']}")])
    
    nav_buttons = []
    if start > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"page:{page-1}"))
    else:
        nav_buttons.append(InlineKeyboardButton(text=" ", callback_data="noop"))
    if end < len(items):
        nav_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"page:{page+1}"))
    else:
        nav_buttons.append(InlineKeyboardButton(text=" ", callback_data="noop"))

    if nav_buttons:
        buttons.append(nav_buttons)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def product_quantity_ik(product_id, quantity) -> InlineKeyboardMarkup:
    buttons = []
    quantity_buttons = []
    
    if quantity > 0:
        quantity_buttons.append(InlineKeyboardButton(
            text="-",
            callback_data=f"item:{product_id}:-"
        ))
    else:
        quantity_buttons.append(InlineKeyboardButton(
            text=" ",
            callback_data="noop"
        ))
    quantity_buttons.append(InlineKeyboardButton(
        text=f"{quantity}",
        callback_data="noop"
        ))
    quantity_buttons.append(InlineKeyboardButton(
        text="+",
        callback_data=f"item:{product_id}:+"
        ))
    buttons.append(quantity_buttons)
    
    buttons.append([InlineKeyboardButton(
        text='✅ Подтвердить',
        callback_data=f'submit:{product_id}'
        )])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)