"""
    Tests for the models in the core application.

"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def create_user(email='user@example.com', password='test@12345'):
    """Helper function to create a user."""
    return get_user_model().objects.create_user(email=email, password=password)


class ModelTests(TestCase):
    """Test cases for the core application models."""

    def test_create_user_with_email_successful(self):
        """ Test creating a user with an email is sucecssful """
        email = "test@example.com"
        password = "testpass123"

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized."""
        sample_emails = [
            ['test1@EXAMPLE.com','test1@example.com'],
            ['Test2@Example.com','Test2@example.com'],
            ['TEST3@EXAMPLE.COM','TEST3@example.com'],
            ['test4@example.COM','test4@example.com']
        ]
        
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email=email, password='sample123')
            self.assertEqual(user.email, expected)



    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email='', password='test123')




    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )  
        self.assertEqual(user.email, 'test@example.com')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


    def test_create_recipe(self):
        """Test creating a recipe is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'test@12345'
        )

        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample Recipe',
            time_minutes=30,
            price=Decimal('5.50'),
            description='Sample description for the recipe.',
        )

        self.assertEqual(str(recipe), recipe.title)


    def test_create_tag(self):
        """Test creating a tag is successful."""
        user = create_user()

        tag = models.Tag.objects.create(
            user=user,
            name='Sample Tag'
        )

        self.assertEqual(str(tag), tag.name)


    def test_create_ingredient(self):
        """Test creating an ingredient is successful."""
        user = create_user()

        ingredient = models.Ingredient.objects.create(
            user=user,
            name='Sample Ingredient'
        )

        self.assertEqual(str(ingredient), ingredient.name)