"""
    Serializer for Recipe model.
"""

from rest_framework import serializers
from core.models import Recipe
from core.models import Tag
from core.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredient model."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)

        

class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model."""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)

        

class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe model."""
    
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'time_minutes', 'price', 'description', 'link',
                   'tags', 'ingredients')
        read_only_fields = ('id',)

    def get_or_create_tags(self, recipe, tags_data):
        """Helper method to get or create tags for a recipe."""
        auth_user = self.context['request'].user
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(user=auth_user, **tag_data)
            recipe.tags.add(tag)
            
    def get_or_create_ingredients(self, recipe, ingredients_data):
        """Helper method to get or create ingredients for a recipe."""
        auth_user = self.context['request'].user
        for ingredient_data in ingredients_data:
            ingredient, created = Ingredient.objects.get_or_create(
                user=auth_user, **ingredient_data)
            recipe.ingredients.add(ingredient)


    def create(self, validated_data):
        """Create a new recipe with tags."""
        tags_data = validated_data.pop('tags', [])
        ingredients_data = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)

        self.get_or_create_tags(recipe, tags_data)
        self.get_or_create_ingredients(recipe, ingredients_data)
        

        return recipe
        
    def update(self, instance, validated_data):
        """Update an existing recipe with tags."""
        tags_data = validated_data.pop('tags', [])
        ingredients_data = validated_data.pop('ingredients', [])

        if tags_data is not None:
            # Clear existing tags if new tags are provided
            instance.tags.clear()
            self.get_or_create_tags(instance, tags_data)

        if ingredients_data is not None:
            # Clear existing ingredients if new ingredients are provided
            instance.ingredients.clear()
            self.get_or_create_ingredients(instance, ingredients_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Save the instance after updating attributes
        instance.save()

        return instance
    

class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for detailed Recipe model."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ('description',)
        read_only_fields = RecipeSerializer.Meta.read_only_fields + ('user',)

