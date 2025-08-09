"""
  url mappings for the recipe api

"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe.views import RecipeViewSet

app_name = 'recipe'

router = DefaultRouter()
router.register('recipes', RecipeViewSet)   

urlpatterns = [
    path('', include(router.urls)),
]