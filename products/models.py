from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass
    

class Product(models.Model):
		# name, price, stock_count
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_count = models.IntegerField(default=0)

    def clean(self):
        if self.price < 0:
            raise ValidationError('Price cannot be negative')
        if self.stock_count < 0:
            raise ValidationError('Stock count cannot be negative')
        
    def get_discount_price(self, discount_percentage):
        """Calculate and return the discounted price."""
        return self.price * (1 - discount_percentage / 100)

    @property
    def in_stock(self):
        """Return True if the product is in stock (i.e., stock_count > 0)."""
        return self.stock_count > 0