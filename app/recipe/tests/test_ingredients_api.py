"""
 test ingredients API

"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status   

from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse('recipe:ingredient-list')

def create_user(email='test@example.com', password='test@12345'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email=email, password=password)


def detail_url(ingredient_id):
    """Create and return a detail URL for an ingredient."""
    return reverse('recipe:ingredient-detail', args=[ingredient_id])


class PublicIngredientsApiTests(TestCase):
    """Test the publicly available ingredients API."""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the ingredients API."""
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
                                                

class PrivateIngredientsApiTests(TestCase):
                                                
    """Test the authorized user ingredients API."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_ingredients(self):
        """Test retrieving a list of ingredients."""
        Ingredient.objects.create(user=self.user, name='Salt')
        Ingredient.objects.create(user=self.user, name='Pepper')

        res = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that ingredients returned are for the authenticated user."""
        other_user = create_user(email='otheruser@example.com', password='otherpass@12345')
        Ingredient.objects.create(user=other_user, name='Sugar')

        ingredient = Ingredient.objects.create(user=self.user, name='Honey')    

        res = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.filter(user=self.user).order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)   

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(serializer.data[0], res.data[0]) 
        self.assertNotIn({'name': 'Sugar'}, res.data)   

    def test_update_ingredient(self):
        """Test updating an ingredient."""
        ingredient = Ingredient.objects.create(user=self.user, name='Butter')
        payload = {'name': 'Olive Oil'}

        url = detail_url(ingredient.id)
        res = self.client.patch(url, payload)

        ingredient.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(ingredient.name, payload['name'])
        self.assertEqual(ingredient.user, self.user)
        

    def test_delete_ingredient(self):
        """Test deleting an ingredient."""
        ingredient = Ingredient.objects.create(user=self.user, name='Garlic')

        url = detail_url(ingredient.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ingredient.objects.filter(id=ingredient.id).exists())

        