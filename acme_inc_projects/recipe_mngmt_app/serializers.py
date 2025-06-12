from rest_framework import serializers
from .models import Ingredient, Recipe


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']


class RecipeSerializer(serializers.ModelSerializer):
    # This field allows us to pass a list of ingredient IDs when creating/updating a recipe
    ingredient_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'ingredient_ids', 'ingredients']

    def create(self, validated_data):
        ingredient_ids = validated_data.pop('ingredient_ids', [])
        recipe = Recipe.objects.create(**validated_data)
        recipe.ingredients.set(ingredient_ids)
        # print("recipe",recipe)
        return recipe

    def update(self, cur_recipe, validated_data):
        ingredient_ids = validated_data.pop('ingredient_ids', None)
        for attr, value in validated_data.items():
            setattr(cur_recipe, attr, value)
        cur_recipe.save()
        if ingredient_ids is not None:
            cur_recipe.ingredients.set(ingredient_ids)

        return cur_recipe