from django.core.exceptions import ValidationError
from django.test import TestCase
from products.models import Product
from django.db import IntegrityError


class ProductModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a sample product for reuse
        cls.product = Product(name="Test Product", price=100.00, stock_count=10)

    def test_in_stock_property(self):
        """Test that the in_stock property returns True if stock_count > 0, False otherwise."""
        self.assertTrue(self.product.in_stock)  # Product with stock should be in stock

        # Set stock_count to 0 and test again
        self.product.stock_count = 0
        self.assertFalse(self.product.in_stock)  # Product with 0 stock should not be in stock

    def test_get_discount_price(self):
        """Test that the get_discount_price method calculates correct discount."""
        self.assertEqual(self.product.get_discount_price(10), 90.00)  # 10% discount on $100 should be $90
        self.assertEqual(self.product.get_discount_price(50), 50.00)  # 50% discount should be $50
        self.assertEqual(self.product.get_discount_price(0), 100.00)  # 0% discount should return original price

    def test_negative_price_constraint(self):
        """Test that a product with a negative price cannot be saved due to the database constraint."""
        product = Product(name="Negative Price Product", price=-1.00, stock_count=5)
        with self.assertRaises(IntegrityError):
            product.save()  # Should raise IntegrityError due to the price_gte_0 constraint

    def test_negative_stock_count_constraint(self):
        """Test that a product with a negative stock count cannot be saved due to the database constraint."""
        product = Product(name="Negative Stock Product", price=50.00, stock_count=-1)
        with self.assertRaises(IntegrityError):
            product.save()  # Should raise IntegrityError due to the stock_count_gte_0 constraint