"""
    Django admin tests for the core application.

"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    """Tests for the Django admin site."""

    def setUp(self):
        """Set up the test client and create a superuser."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="superusertest@example.com",
            password="test@12345"
        )
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email="testuser@example.com",
            password="test@12345",
            name="Test User")
        

    def test_users_listed(self):
        """Test that users are listed on the user page."""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)

    def test_edit_user_page(self):
        """Test that the edit user page works."""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)

    def test_create_user_page(self):
        """Test that the create user page works."""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Add user')