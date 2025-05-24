from aiogram.fsm.state import State, StatesGroup


class CatalogStates(StatesGroup):
    selecting_category = State()
    selecting_brand = State()
    selecting_car = State()


class CartStates(StatesGroup):
    viewing_cart = State()


class UserInfoStates(StatesGroup):
    waiting_for_address = State()
    waiting_for_phone = State()