from django.db import models
from django.contrib.auth.models import AbstractUser


# Пользователь
class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username


# Категория автомобилей
class CarCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Марка автомобилей
class CarBrand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Автомобиль
class Car(models.Model):
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, related_name="cars")
    category = models.ForeignKey(CarCategory, on_delete=models.CASCADE, related_name="cars")
    model_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    year = models.PositiveIntegerField()
    mileage = models.PositiveIntegerField()
    image = models.ImageField(upload_to='cars/', default='cars/nophoto.jpg')

    def __str__(self):
        return f"{self.brand} {self.model_name}"


# Корзина
class Cart(models.Model):
    order_id = models.BigIntegerField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="carts")
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    is_payed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} — {self.car.model_name}"
