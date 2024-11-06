from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from products.models import Product

class TestHomePage(SimpleTestCase):

    def test_homepage_uses_correct_template(self):
        """Test that the homepage view uses the correct template."""
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'index.html')

    def test_homepage_contains_welcome_message(self):
        """Test that the homepage contains the welcome message in the content."""
        response = self.client.get(reverse('home'))
        self.assertContains(
            response,
            'Welcome to our Store!',
            status_code=200
        )

class TestProductsPage(TestCase):
    def setUp(self):
        """Create some products for testing."""
        Product.objects.create(name="Laptop", price=1000)
        Product.objects.create(name="Phone", price=800)

    def test_products_uses_correct_template(self):
        """Test that the products view uses the correct template."""
        response = self.client.get(reverse('products'))
        self.assertTemplateUsed(response, 'products.html')

    def test_products_context(self):
        """Test that the products context contains the correct products."""
        response = self.client.get(reverse('products'))
        self.assertEqual(len(response.context['products']), 2)
        self.assertContains(response, 'Laptop')
        self.assertContains(response, 'Phone')
        self.assertNotContains(response, 'No products available')

    def test_products_view_no_products(self):
        """Test that the view behaves correctly when no products are available."""
        Product.objects.all().delete()  # Clear all products
        response = self.client.get(reverse('products'))
        self.assertEqual(len(response.context['products']), 0)
        self.assertContains(response, 'No products available')
