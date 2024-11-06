from django.test import SimpleTestCase
from django.urls import reverse

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