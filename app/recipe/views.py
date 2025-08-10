"""
    views for the recipe api

"""

from rest_framework import (viewsets, mixins)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from recipe import serializers

from core.models import Recipe
from core.models import Tag
from core.models import Ingredient

class RecipeViewSet(viewsets.ModelViewSet):
    """Viewset for Recipe API."""
    
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self): 
        """Retrieve the recipes for the authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')
    
    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class
    
    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user) 


class BaseRecipeAtrrViewSet(mixins.DestroyModelMixin, 
                             mixins.UpdateModelMixin, 
                             mixins.ListModelMixin, 
                             viewsets.GenericViewSet):
    """Base viewset for recipe attributes."""
    serializer_class = None
    queryset = None 

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,) 

    def get_queryset(self):
        """Retrieve the attributes for the authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')
    
        
    
class TagViewSet(BaseRecipeAtrrViewSet):
    """Viewset for Tag API."""
    
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


    
class IngredientViewSet(BaseRecipeAtrrViewSet):
    """Viewset for Ingredient API."""
    
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
