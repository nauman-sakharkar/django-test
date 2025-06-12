import strawberry
import strawberry_django
from .models import Ingredient, Recipe
from typing import List
from strawberry.types import Info
from .serializers import IngredientSerializer, RecipeSerializer
# from strawberry.permission import BasePermission

# class IsAuthenticated(BasePermission):
#     message = "You must be authenticated to access this resource."

#     def has_permission(self, source, info: Info, **kwargs) -> bool:
#         # print("info.context.request.user.is_authenticated",info.context.request.user.is_authenticated)
#         return info.context.request.user.is_authenticated

# Defined Objects
@strawberry_django.type(Ingredient)
class IngredientType:
    id: strawberry.auto
    name: strawberry.auto


@strawberry_django.type(Recipe)
class RecipeType:
    id: strawberry.auto
    title: strawberry.auto
    ingredients: List[IngredientType]

    @strawberry.field
    def ingredient_count(self) -> int:
        return self.ingredients.count()


# Defined query functions
@strawberry.type
class Query:
    @strawberry_django.field
    def get_ingredients(self) -> List[IngredientType]:
        return Ingredient.objects.all()

    @strawberry_django.field
    def get_recipe(self, id: int) -> RecipeType:
        return Recipe.objects.get(pk=id)



# Mutations
@strawberry_django.input(Ingredient)
class IngredientInput:
    name: strawberry.auto

@strawberry.input
class RecipeInput:
    title: str
    ingredient_ids: List[int]

@strawberry.type
class Mutation:

    # Ingredient CRUD
    @strawberry.field
    def insert_ingredient(self, info: Info, input: IngredientInput) -> IngredientType:
        serializer = IngredientSerializer(data=input.__dict__)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @strawberry.field
    def update_ingredient(self, info: Info, id: int, input: IngredientInput) -> IngredientType:
        ingredient = Ingredient.objects.get(pk=id)
        serializer = IngredientSerializer(ingredient, data=input.__dict__)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @strawberry.field
    def delete_ingredient(self, info: Info, id: int) -> bool:
        Ingredient.objects.get(pk=id).delete()
        return True
    

    # Recipe CRUD
    @strawberry_django.mutation
    def insert_recipe(self, info: Info, input: RecipeInput) -> RecipeType:
        serializer = RecipeSerializer(data=input.__dict__)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @strawberry_django.mutation
    def add_ingredient_to_recipe(self, recipe_id: int, ingredient_id: int) -> RecipeType:
        recipe = Recipe.objects.get(pk=recipe_id)
        recipe.ingredients.add(ingredient_id)
        return recipe

    @strawberry_django.mutation
    def remove_ingredient_from_recipe(self, recipe_id: int, ingredient_id: int) -> RecipeType:
        recipe = Recipe.objects.get(pk=recipe_id)
        recipe.ingredients.remove(ingredient_id)
        return recipe
    


schema = strawberry.Schema(query=Query, mutation=Mutation)