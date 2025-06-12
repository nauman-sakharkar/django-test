from rest_framework import viewsets
from .models import Ingredient, Recipe
from .serializers import IngredientSerializer, RecipeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer



class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer



class AddIngredientToRecipeView(APIView):
    def post(self, request):
        recipe_id = request.data.get('recipe_id')
        ingredient_id = request.data.get('ingredient_id')
        recipe = Recipe.objects.get(id=recipe_id)
        ingredient = Ingredient.objects.get(id=ingredient_id)
        recipe.ingredients.add(ingredient)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_200_OK)