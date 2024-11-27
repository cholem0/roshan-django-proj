from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.BigIntegerField(null=True)
    visits = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, related_name='cart', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"