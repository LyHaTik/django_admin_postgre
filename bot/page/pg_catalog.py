from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.fsm.context import FSMContext

from keyboards.kb_catalog import paginated_ik, product_quantity_ik
from config import bot


# Страница "Категории"
async def categories_page(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    categories = data.get('categories')
    
    text = "Выберите категорию:"
    reply_markup = await paginated_ik(items=categories)
    await message.answer(text, reply_markup=reply_markup)


# Страница "Подкатегории"
async def subcategories_page(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    subcategories = data.get('subcategories')
    
    if not subcategories:
        await callback.answer("Нет товаров", show_alert=True)
        return
    
    text = "Выберите подкатегорию:"
    reply_markup = await paginated_ik(items=subcategories)
    await callback.message.edit_text(text=text, reply_markup=reply_markup)


# Страница "Продукты"
async def products_page(callback: CallbackQuery, state: FSMContext, page: int=1):
    await callback.message.delete()
    chat_id = callback.message.chat.id

    data = await state.get_data()
    products = data.get('products')
    
    if not products:
        await callback.answer("Нет товаров", show_alert=True)
        return
    
    product = products[page - 1]

    reply_markup = await paginated_ik(items=products, page=page, per_page=1)
    photo = FSInputFile(product['image'])
    caption = f"{product['name']}\nЦена: {product['price']}₽"

    await bot.send_photo(chat_id=chat_id, photo=photo, caption=caption, reply_markup=reply_markup)


# Страница "Выбранного продукта"
async def product_page(callback: CallbackQuery, product_id: int, quantity: int):
    
    reply_markup = await product_quantity_ik(product_id=product_id, quantity=quantity)
    await callback.message.edit_reply_markup(reply_markup=reply_markup)

