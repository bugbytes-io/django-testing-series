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

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(price__gte=0), name='price_gt_0'),
            models.CheckConstraint(condition=models.Q(stock_count__gte=0), name='stock_gt_0'),
        ]
        
    def get_discount_price(self, discount_percentage):
        """Calculate and return the discounted price."""
        return self.price * (1 - discount_percentage / 100)

    @property
    def in_stock(self):
        """Return True if the product is in stock (i.e., stock_count > 0)."""
        return self.stock_count > 0