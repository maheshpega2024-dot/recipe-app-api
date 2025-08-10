"""
    this is for testing the tags API

"""
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from core.models import Recipe

from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')

def details_url(tag_id):
    """Return tag detail URL."""
    return reverse('recipe:tag-detail', args=[tag_id])



def create_user(email='user@example.com', password='test@12345'):
    """Helper function to create a user."""
    return get_user_model().objects.create_user(email=email, password=password)



class PublicTagsApiTests(TestCase):
    
    """Test the publicly available tags API."""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the tags API."""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test the authorized user tags API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags."""
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)



    def test_tags_limited_to_user(self):
        """Test that tags returned are for the authenticated user."""
        other_user = create_user(email='test@example.com', password='test@12345')
        Tag.objects.create(user=other_user, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='Comfort Food')

        res = self.client.get(TAGS_URL)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0]['id'], tag.id)

    
    def test_update_tag(self):
        """Test updating a tag."""
        tag = Tag.objects.create(user=self.user, name='After Dinner')

        payload = {'name': 'Brunch'}
        url = details_url(tag.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])

    
    def test_delete_tag(self):
        """Test deleting a tag."""
        tag = Tag.objects.create(user=self.user, name='Breakfast')

        url = details_url(tag.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tag.objects.filter(user=self.user).exists())

 
    def test_filter_tags_assigned_to_recipes(self):
        """Test listing tags assigned to recipes."""
        tag1 = Tag.objects.create(user=self.user, name='Breakfast')
        tag2 = Tag.objects.create(user=self.user, name='Dinner')
        recipe = Recipe.objects.create(
            title='Spicy Curry',
            time_minutes=30,
            price=Decimal('5.99'),
            user=self.user
        )
        recipe.tags.add(tag1)

        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        serializer1 = TagSerializer(tag1)
        serializer2 = TagSerializer(tag2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_filtered_tags_unique(self):
        """Test that filtered tags returns unique items."""
        tag1 = Tag.objects.create(user=self.user, name='Cumin')
        Tag.objects.create(user=self.user, name='Coriander')
        recipe1 = Recipe.objects.create(
            title='Spicy Curry',
            time_minutes=30,
            price=Decimal('5.99'),
            user=self.user
        )
        recipe1.tags.add(tag1)
        recipe2 = Recipe.objects.create(
            title='Curry Rice',
            time_minutes=20,
            price=Decimal('4.99'),
            user=self.user
        )
        recipe2.tags.add(tag1)

        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)
        
    