from aiogram.fsm.state import State, StatesGroup


class CatalogStates(StatesGroup):
    selecting_category = State()
    selecting_subcategory = State()
    selecting_product = State()


class CartStates(StatesGroup):
    viewing_cart = State()


class UserInfoStates(StatesGroup):
    waiting_for_address = State()
    waiting_for_phone = State()