from handlers.hand_start import register_start
from handlers.hand_catalog import register_catalog
from handlers.hand_cart import register_cart
from handlers.hand_payment import register_payment
from handlers.hand_faq import register_faq
from handlers.hand_user_contact import register_user_contact


def register_all_handlers(dp):
    register_start(dp)
    register_catalog(dp)
    register_cart(dp)
    register_payment(dp)
    register_faq(dp)
    register_user_contact(dp)
