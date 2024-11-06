from django.test import SimpleTestCase, TestCase, tag
from django.urls import reverse
from products.models import Product, User

class TestProfilePage(TestCase):    
    def test_profile_view_redirects_for_anonymous_users(self):
        """Test that anonymous users are redirected to the login page when trying to access the profile view."""
        response = self.client.get(reverse('profile'))
        
        # Check if the user was redirected to the login page
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('profile')}")

    @tag('auth')
    def test_profile_view_accessible_for_authenticated_users(self):
        """Test that authenticated users can access the profile view and see their username."""
        # Create a test user
        User.objects.create_user(username='testuser', password='password123')

        # Log the user in
        self.client.login(username='testuser', password='password123')

        # Access the profile page
        response = self.client.get(reverse('profile'))

        # Check that the response status code is 200 (successful access)
        self.assertEqual(response.status_code, 200)

        # Check if the user's username is in the response content
        self.assertContains(response, 'testuser')

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

from unittest.mock import patch
import requests

class PostsViewTest(TestCase):

    @patch('products.views.requests.get')
    def test_post_view_success(self, mock_get):
        """Test that the posts view returns valid JSON for a successful response."""
        
        # Simulate a successful response with status code 200
        mock_get.return_value.status_code = 200
        return_data = {
            "userId": 1,
            "id": 1,
            "title": "Test Title",
            "body": "Test Body"
        }
        mock_get.return_value.json.return_value = return_data

        # Send a request to the view
        response = self.client.get(reverse('post'))

        # Check if the response status is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the view returns the mocked JSON data
        self.assertJSONEqual(response.content, return_data)

        # Ensure that the mock API call was made once with the correct URL
        mock_get.assert_called_once_with('https://jsonplaceholder.typicode.com/posts/1')


    @patch('products.views.requests.get')
    def test_post_view_fail(self, mock_get):
        """Test that the posts view returns 503 on HTTP errors."""

        # Simulate a failure (e.g., a network error)
        # https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.side_effect
        mock_get.side_effect = requests.exceptions.RequestException

        # Send a request to the view
        response = self.client.get(reverse('post'))

        # Check that the view returns a 503 Service Unavailable status code
        self.assertEqual(response.status_code, 503)

        # Ensure the external API was called once
        mock_get.assert_called_once_with('https://jsonplaceholder.typicode.com/posts/1')