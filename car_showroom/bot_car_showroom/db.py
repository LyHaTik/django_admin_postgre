from asgiref.sync import sync_to_async
from .models import CarCategory, CarBrand, Car, Cart, User


@sync_to_async(thread_sensitive=True)
def create_user(user_id: int):
    _, created = User.objects.get_or_create(id=user_id)
    return created

@sync_to_async(thread_sensitive=True)
def get_categories():
    return list(CarCategory.objects.all())

@sync_to_async(thread_sensitive=True)
def get_brands():
    return list(CarBrand.objects.all())

@sync_to_async(thread_sensitive=True)
def get_cars(category_id: int, brand_id: int):
    return list(Car.objects.select_related("brand").filter(category_id=category_id, brand_id=brand_id))

@sync_to_async(thread_sensitive=True)
def get_car(car_id: int):
    return Car.objects.select_related("brand").filter(id=car_id).first()

@sync_to_async(thread_sensitive=True)
def get_cart(user_id: int):
    return list(Cart.objects.select_related('car__brand').filter(user_id=user_id, is_payed=False))

@sync_to_async(thread_sensitive=True)
def put_car_to_cart(user_id: int, car_id: int, quantity: int):
    item, created = Cart.objects.get_or_create(user_id=user_id, car_id=car_id, is_payed=False, defaults={"quantity": quantity})
    if not created:
        item.quantity += quantity
        item.save()

@sync_to_async(thread_sensitive=True)
def put_order_id_to_cart(cart, order_id):
    for item in cart:
        item.order_id = order_id
        item.save()

@sync_to_async(thread_sensitive=True)
def change_quantity_to_cart(user_id: int, car_id: int, quantity: int):
    item = Cart.objects.filter(user_id=user_id, car_id=car_id, is_payed=False).first()
    if item:
        item.quantity = quantity
        item.save()

@sync_to_async(thread_sensitive=True)
def delete_item_to_cart(user_id: int, car_id: int):
    item = Cart.objects.filter(user_id=user_id, car_id=car_id, is_payed=False).first()
    if item:
        item.delete()

@sync_to_async(thread_sensitive=True)
def clean_cart(user_id: int):
    Cart.objects.filter(user_id=user_id, is_payed=False).delete()

@sync_to_async(thread_sensitive=True)
def get_user_data_from_db(user_id: int):
    return User.objects.filter(id=user_id).first()

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
def mark_item_as_payed(item):
    item.is_payed = True
    item.save()