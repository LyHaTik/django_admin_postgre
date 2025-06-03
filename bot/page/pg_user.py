from aiogram.types import CallbackQuery, Message

from keyboards.kb_main_menu import get_phone_request_rk, main_menu_rk


async def welcome_page(text: str, message: Message, reply_markup=main_menu_rk()):
    await message.answer(text=text, reply_markup=reply_markup)


async def send_address(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        text="Перед оплатой, пожалуйста, напишите ваш адрес для доставки."
    )


async def send_phone(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        text="Перед оплатой, пожалуйста, добавьте телефон (кнопкой).",
        reply_markup=get_phone_request_rk()
    )


async def error_phone(message: Message):
    await message.answer(
        text="Пожалуйста, отправьте свой номер через кнопку.",
        reply_markup=get_phone_request_rk()
    )


async def phone_ok(message: Message):
    await message.answer(
        text="Телефон сохранён ✅",
        reply_markup=main_menu_rk()
    )


async def address_ok(message: Message):  
    await message.answer(
        text="Адрес сохранён ✅",
        reply_markup=main_menu_rk()
    )
