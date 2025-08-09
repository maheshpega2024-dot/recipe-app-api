"""
    Serializer for Recipe model.
"""

from rest_framework import serializers
from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe model."""

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'time_minutes', 'price', 'description', 'link')
        read_only_fields = ('id',)
        
class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for detailed Recipe model."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ('description',)
        read_only_fields = RecipeSerializer.Meta.read_only_fields + ('user',)
