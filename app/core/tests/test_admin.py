"""
Tests for the Django Admin modifications
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

class AdminSiteTests(TestCase):
    """Test for the Django Admin """

    def setUp(self):
        """Create a user and client we are creating two user and checking"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = "admin@example.com",
            password = "testpass123"
            
        )

        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email = "user@example.com",
            password = "testpass123",
            name = "Test User",
        )

    def test_user_list(self):
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)


    def test_edit_user_page(self):
        """Test the edit_user page works properly"""
        url = reverse('admin:core_user_change', args= [self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create_user page works properly"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

