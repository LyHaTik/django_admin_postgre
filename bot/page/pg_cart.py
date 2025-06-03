
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from db.db_cart import get_cart
from keyboards.kb_cart import cart_ik


# Страница "Корзина"
async def cart_page(user_id: int, state: FSMContext, message_or_callback: Message | CallbackQuery):
    cart_list = await get_cart(user_id)

    if not cart_list:
        await state.clear()
        text = "🛒 Корзина пуста."
        if isinstance(message_or_callback, Message):
            await message_or_callback.answer(text)
        else:
            if message_or_callback.message:
                await message_or_callback.message.delete()
            await message_or_callback.answer(text, show_alert=True)
        return

    reply_markup = await cart_ik(cart_list)
    text = "🛒 Ваша корзина оформлена:\n"

    if isinstance(message_or_callback, Message):
        await message_or_callback.delete()
        await message_or_callback.answer(text, reply_markup=reply_markup)
    else:
        await message_or_callback.message.delete()
        await message_or_callback.message.answer(text, reply_markup=reply_markup)
