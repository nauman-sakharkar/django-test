from django.contrib import admin
from django.urls import path, include
from strawberry.django.views import GraphQLView
from recipe_mngmt_app.schema import schema
from rest_framework.routers import DefaultRouter
from recipe_mngmt_app.views import IngredientViewSet, RecipeViewSet, AddIngredientToRecipeView
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("graphql/", GraphQLView.as_view(schema=schema)),
    path('api/', include(router.urls)),
    path('api/add-ingredient-to-recipe/', AddIngredientToRecipeView.as_view(), name='add-ingredient-to-recipe'),
    path('api/token/', obtain_auth_token, name='api_token_auth'),
]