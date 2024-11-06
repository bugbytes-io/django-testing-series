from django.test import TestCase
from unittest.mock import patch
from products.models import User

class UserSignalsTest(TestCase):

    @patch('products.signals.send_mail')
    def test_welcome_email_sent_on_user_creation(self, mock_send_mail):
        # Create a new user, which should trigger the signal
        User.objects.create_user(username='john', email='john@example.com', password='password123')

        # Check that send_mail was called once
        mock_send_mail.assert_called_once_with(
            'Welcome!',
            'Thanks for signing up!',
            'admin@django.com',
            ['john@example.com'],
            fail_silently=False
        )

    @patch('products.signals.send_mail')
    def test_no_email_sent_on_user_update(self, mock_send_mail):
        # Create a new user, which should trigger the signal
        user = User.objects.create_user(username='john', email='john@example.com', password='password123')

        # Reset the mock call count to zero
        mock_send_mail.reset_mock()

        # Update the user (the signal should not send an email this time)
        user.email = 'john_new@example.com'
        user.save()

        # Ensure send_mail was not called
        mock_send_mail.assert_not_called()