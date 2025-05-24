from .start import register_start
from .catalog import register_catalog
from .cart import register_cart
from .payment import register_payment
from .pagination import register_pagination
from .faq import register_faq
from .main_menu import register_main_menu
from .user_contact import register_user_contact


def register_all_handlers(dp):
    register_start(dp)
    register_catalog(dp)
    register_cart(dp)
    register_payment(dp)
    register_pagination(dp)
    register_faq(dp)
    register_main_menu(dp)
    register_user_contact(dp)