"""
# This file is part of the recipe-app-api project.
"""

from decimal import Decimal


from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import  Recipe, Tag, Ingredient
    

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """Create and return a recipe detail URL."""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def create_recipe(user, **params):
    """Create and return a sample recipe."""
    defaults = {
        'title': 'Sample Recipe',
        'time_minutes': 10,
        'price': Decimal('5.00'),
        'description': 'Sample description',
        'link': 'http://example.com/recipe.pdf',
    }
    defaults.update(params)

    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe

def create_user(**params):
    """Create and return a sample user."""
    return get_user_model().objects.create_user(**params)

class PublicRecipeApiTests(TestCase):
    """Test unauthenticated recipe API access."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required to access the recipe API."""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """Test authenticated recipe API access."""

    def setUp(self):
        self.user = create_user(email='test@example.com', password='test@12345')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes."""
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        #descending order by id
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    
    def test_retrieve_recipes_limited_to_user(self):
        """Test retrieving recipes for the authenticated user."""

        other_user = create_user(email='otheruser@example.com', password='test@12345')
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user).order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_detail(self):
        """Test getting recipe detail."""
        recipe = create_recipe(user=self.user)

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """Test creating a recipe."""
        payload = {
            'title': 'New Recipe',
            'time_minutes': 30,
            'price': Decimal('10.00'),
            'description': 'New recipe description',
            'link': 'http://example.com/new-recipe.pdf',
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

        self.assertEqual(recipe.user, self.user)


    def test_partial_update_recipe(self):
        """Test partially updating a recipe."""
        original_title = 'Original Title'
        recipe = create_recipe(user=self.user, title=original_title)

        payload = {'title': 'Updated Title'}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.user, self.user)


    def test_full_update_recipe(self):
        """Test fully updating a recipe."""
        recipe = create_recipe(user=self.user)

        payload = {
            'title': 'Updated Recipe',
            'time_minutes': 20,
            'price': Decimal('8.00'),
            'description': 'Updated description',
            'link': 'http://example.com/updated-recipe.pdf',
        }
        url = detail_url(recipe.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))
        self.assertEqual(recipe.user, self.user)

    def test_update_user_recipe_error(self):
        """Test updating a recipe with a different user fails."""
        other_user = create_user(email='test3@example.com', password='test@12345')
        recipe = create_recipe(user=other_user)

        payload = {'user': 'testuser@example.com'}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)


        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        recipe.refresh_from_db()
        self.assertEqual(recipe.user, other_user)
        

    def test_delete_recipe(self):   
        """Test deleting a recipe."""
        recipe = create_recipe(user=self.user)

        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

    def test_delete_other_user_recipe_error(self):
        """Test trying to delete a recipe of another user fails."""
        new_user = create_user(email='newuser@example.com', password='test@12345')
        recipe = create_recipe(user=new_user)

        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id=recipe.id).exists())


    def test_create_recipe_with_new_tags(self):
        """Test creating a recipe with new tags."""
        payload = {
            'title': 'Recipe with Tags',
            'time_minutes': 15,
            'price': Decimal('7.50'),
            'tags': [{'name': 'Thai'}, {'name': 'Dinner'}],
        }

        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipes = Recipe.objects.filter(
            user=self.user
        )
        self.assertEqual(recipes.count(), 1)

        recipe = recipes[0]
        self.assertEqual(recipe.tags.count(), 2)
        for tag in payload['tags']:
            exists = recipe.tags.filter(name=tag['name']).exists()
            self.assertTrue(exists)

    def test_create_recipe_with_existing_tags(self):
        """Test creating a recipe with existing tags."""
        tag_1 = Tag.objects.create(user=self.user, name='Breakfast')
        tag_2 = Tag.objects.create(user=self.user, name='Lunch')

        payload = {
            'title': 'Recipe with Existing Tags',
            'time_minutes': 20,
            'price': Decimal('9.00'),
            'tags': [{'name': 'Breakfast'}, {'name': 'Lunch'}],
        }

        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipes = Recipe.objects.filter(
            user=self.user
        )
        self.assertEqual(recipes.count(), 1)

        recipe = recipes[0]
        self.assertEqual(recipe.tags.count(), 2)
        self.assertIn(tag_1, recipe.tags.all())
        self.assertIn(tag_2, recipe.tags.all())

        for tag in payload['tags']:
            exists = recipe.tags.filter(name=tag['name']).exists()
            self.assertTrue(exists)

    
    def test_create_tag_on_update(self):
        """Test creating a tag when updating a recipe."""
        recipe = create_recipe(user=self.user)

        payload = {
            'tags': [{'name': 'Brunch'}],
        }
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        recipe.refresh_from_db()

        new_tag = Tag.objects.get(user=self.user, name='Brunch')
        self.assertIn(new_tag, recipe.tags.all())   

    def test_update_recipe_assign_tag(self):
        """Test assigning an existing tag when updating a recipe."""
        tag_1 = Tag.objects.create(user=self.user, name='Dessert')
        recipe = create_recipe(user=self.user)
        recipe.tags.add(tag_1)

        tag_2 = Tag.objects.create(user=self.user, name='Snack')
        payload = {
            'tags': [{'name': 'Snack'}],
        }
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe.refresh_from_db()
        self.assertIn(tag_2, recipe.tags.all())
        self.assertNotIn(tag_1, recipe.tags.all())


    def test_clear_recipe_tags(self):
        """Test clearing tags from a recipe."""
        tag_1 = Tag.objects.create(user=self.user, name='Vegan')
        tag_2 = Tag.objects.create(user=self.user, name='Gluten-Free')

        recipe = create_recipe(user=self.user)
        recipe.tags.add(tag_1)
        recipe.tags.add(tag_2)

        payload = {'tags': []}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe.refresh_from_db()
        self.assertEqual(recipe.tags.count(), 0)


    def test_create_recipe_with_new_ingredients(self):
        """Test creating a recipe with new ingredients."""
        payload = {
            'title': 'Recipe with Ingredients',
            'time_minutes': 25,
            'price': Decimal('12.50'),
            'ingredients': [{'name': 'Chicken'}, {'name': 'Rice'}],
        }

        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipes = Recipe.objects.filter(
            user=self.user
        )
        self.assertEqual(recipes.count(), 1)

        recipe = recipes[0]
        self.assertEqual(recipe.ingredients.count(), 2)
        for ingredient in payload['ingredients']:
            exists = recipe.ingredients.filter(name=ingredient['name'], user=self.user).exists()
            self.assertTrue(exists)

    def test_create_recipe_with_existing_ingredients(self): 
        """Test creating a recipe with existing ingredients."""
        ingredient_1 = Ingredient.objects.create(user=self.user, name='Eggs')
        ingredient_2 = Ingredient.objects.create(user=self.user, name='Bacon')

        payload = {
            'title': 'Recipe with Existing Ingredients',
            'time_minutes': 30,
            'price': Decimal('15.00'),
            'ingredients': [{'name': 'Eggs'}, {'name': 'Bacon'}],
        }

        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipes = Recipe.objects.filter(
            user=self.user
        )
        self.assertEqual(recipes.count(), 1)

        recipe = recipes[0]
        self.assertEqual(recipe.ingredients.count(), 2)
        self.assertIn(ingredient_1, recipe.ingredients.all())
        self.assertIn(ingredient_2, recipe.ingredients.all())

        for ingredient in payload['ingredients']:
            exists = recipe.ingredients.filter(name=ingredient['name'], user=self.user).exists()
            self.assertTrue(exists)


    def test_create_ingredient_on_update(self):
        """Test creating an ingredient when updating a recipe."""
        recipe = create_recipe(user=self.user)

        payload = {
            'ingredients': [{'name': 'Lettuce'}],
        }
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        recipe.refresh_from_db()

        new_ingredient = Ingredient.objects.get(user=self.user, name='Lettuce')
        self.assertIn(new_ingredient, recipe.ingredients.all())

    
    def test_update_recipe_assign_ingredient(self):
        """Test assigning an existing ingredient when updating a recipe."""
        ingredient_1 = Ingredient.objects.create(user=self.user, name='Tomato')
        recipe = create_recipe(user=self.user)
        recipe.ingredients.add(ingredient_1)

        ingredient_2 = Ingredient.objects.create(user=self.user, name='Cucumber')
        payload = {
            'ingredients': [{'name': 'Cucumber'}],
        }
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe.refresh_from_db()
        self.assertIn(ingredient_2, recipe.ingredients.all())
        self.assertNotIn(ingredient_1, recipe.ingredients.all())

    def test_clear_recipe_ingredients(self):    
        """Test clearing ingredients from a recipe."""
        ingredient_1 = Ingredient.objects.create(user=self.user, name='Cheese')
        ingredient_2 = Ingredient.objects.create(user=self.user, name='Bread')

        recipe = create_recipe(user=self.user)
        recipe.ingredients.add(ingredient_1)
        recipe.ingredients.add(ingredient_2)

        payload = {'ingredients': []}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe.refresh_from_db()
        self.assertEqual(recipe.ingredients.count(), 0)