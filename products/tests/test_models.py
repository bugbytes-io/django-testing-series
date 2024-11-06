from django.core.exceptions import ValidationError
from django.test import TestCase
from products.models import Product

class ProductModelTest(TestCase):

    def setUp(self):
        # Create a sample product for reuse
        self.product = Product(name="Test Product", price=100.00, stock_count=10)

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

    def test_negative_price_validation(self):
        """Test that a product with a negative price raises a ValidationError."""
        product = Product(name="Negative Price Product", price=-10.00, stock_count=5)
        with self.assertRaises(ValidationError):
            product.clean()  # This should raise a ValidationError due to negative price

    def test_negative_stock_count_validation(self):
        """Test that a product with a negative stock count raises a ValidationError."""
        product = Product(name="Negative Stock Product", price=10.00, stock_count=-5)
        with self.assertRaises(ValidationError):
            product.clean()  # This should raise a ValidationError due to negative stock count
