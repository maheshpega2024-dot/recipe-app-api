"""
  url mappings for the recipe api

"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe.views import RecipeViewSet
from recipe.views import TagViewSet
from recipe.views import IngredientViewSet

app_name = 'recipe'

router = DefaultRouter()
router.register('recipes', RecipeViewSet)   
router.register('tags', TagViewSet) 
router.register('ingredients', IngredientViewSet) 

urlpatterns = [
    path('', include(router.urls)),
]