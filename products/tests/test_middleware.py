from django.test import TestCase, override_settings
from django.urls import reverse


class MaintenanceModeTests(TestCase):

    @override_settings(MAINTENANCE_MODE=True)
    def test_maintenance_mode_on(self):
        """Test that the site returns a maintenance response when MAINTENANCE_MODE is True."""
        
        # Simulate a request to the homepage
        response = self.client.get(reverse('home'))
        
        # Check the response status code and content
        self.assertContains(response, "Site is under maintenance", status_code=503)


    @override_settings(MAINTENANCE_MODE=False)
    def test_maintenance_mode_off(self):
        """Test that the site works normally when MAINTENANCE_MODE is False."""
        
        # Simulate a request to the homepage
        response = self.client.get(reverse('home'))
        
        # Check that the response is successful and normal content is returned
        self.assertContains(response, "Welcome to our Store!", status_code=200)