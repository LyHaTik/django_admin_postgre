from asgiref.sync import sync_to_async
from .models import Category, SubCategory, Product, Cart, User, MailingMessage


@sync_to_async(thread_sensitive=True)
def create_user(user_id: int) -> bool:
    _, created = User.objects.get_or_create(id=user_id)
    return created

@sync_to_async(thread_sensitive=True)
def get_categories() -> list:
    return list(Category.objects.all())

@sync_to_async(thread_sensitive=True)
def get_subcategories(category_id: int) -> list:
    return list(SubCategory.objects.select_related("category").filter(category_id=category_id))

@sync_to_async(thread_sensitive=True)
def get_products(subcategory_id: int) -> list:
    return list(Product.objects.select_related("subcategory").filter(subcategory_id=subcategory_id))

@sync_to_async(thread_sensitive=True)
def put_product_to_cart(user_id: int, product_id: int, quantity: int):
    item, created = Cart.objects.get_or_create(user_id=user_id, product_id=product_id, is_payed=False, defaults={"quantity": quantity})
    if not created:
        item.quantity += quantity
        item.save()

@sync_to_async(thread_sensitive=True)
def change_quantity_to_cart(user_id: int, product_id: int, quantity: int):
    item = Cart.objects.filter(user_id=user_id, product_id=product_id, is_payed=False).first()
    if item:
        item.quantity = quantity
        item.save()

@sync_to_async(thread_sensitive=True)
def get_cart(user_id: int) -> list:
    return list(Cart.objects.select_related('product__subcategory').filter(user_id=user_id, is_payed=False))

@sync_to_async(thread_sensitive=True)
def delete_item_to_cart(user_id: int, product_id: int):
    item = Cart.objects.filter(user_id=user_id, product_id=product_id, is_payed=False).first()
    if item:
        item.delete()

@sync_to_async(thread_sensitive=True)
def clean_cart(user_id: int):
    Cart.objects.filter(user_id=user_id, is_payed=False).delete()

@sync_to_async(thread_sensitive=True)
def put_order_id_to_cart(cart: list, order_id: int):
    for item in cart:
        item.order_id = order_id
        item.save()
        
@sync_to_async(thread_sensitive=True)
def update_user_address(user_id: int, address: str):
    user = User.objects.filter(id=user_id).first()
    user.address = address
    user.save()        
        
@sync_to_async(thread_sensitive=True)
def update_user_phone(user_id: int, phone: str):
    user = User.objects.filter(id=user_id).first()
    user.phone = phone
    user.save()  

@sync_to_async(thread_sensitive=True)
def get_user_data_from_db(user_id: int) -> User:
    return User.objects.filter(id=user_id).first()

@sync_to_async(thread_sensitive=True)
def get_product(product_id: int) -> Product:
    return Product.objects.select_related("subcategory").filter(id=product_id).first()

@sync_to_async(thread_sensitive=True)
def mark_item_as_payed(item: Cart):
    item.is_payed = True
    item.save()

@sync_to_async(thread_sensitive=True)
def mailing_text() -> str:
    mm = MailingMessage.objects.filter(is_sent=False).first()
    if mm:
        mm.is_sent = True
        mm.save()
        return mm.text
    return None