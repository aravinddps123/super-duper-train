"""
Test for the Models
"""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def create_user(email='user@example.com', password='testpass123'):
    """Create a new user and return"""
    return get_user_model().objects.create_user(email, password)


class ModelsTests(TestCase):
    """Test Models """

    def test_create_user_with_email_successful(self):
        """test created user with email successful"""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email, password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """test is the email is normalized for new users"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', "test123")

    def test_create_superuser(self):

        user = get_user_model().objects.create_superuser(

            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """test creating a recipe is successful or not"""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123'
        )

        recipe = models.Recipe.objects.create(
            user=user,
            title='Name of recipe',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Sample recipe description',

        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """test creating a tag is successful or not"""
        user = create_user()
        tag = models.Tag.objects.create(user=user, tag_name='Tag1')

        self.assertEqual(str(tag), tag.name)

    def test_create_tag(self):
        """Test creating a tag is successful or not"""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag1')

        self.assertEqual(str(tag), tag.name)
