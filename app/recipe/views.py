"""
    views for the recipe api

"""

from rest_framework import (viewsets, mixins, status)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response


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
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class
    
    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user) 

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a recipe."""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            image = request.FILES.get('image')
            if not image:
                return Response({'error': 'Image file is required.'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save(image=image)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
