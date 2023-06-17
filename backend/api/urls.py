"""Эндпойнты приложения YaMDb."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (DownloadShoppingCart, FavoriteViewSet, IngredientViewSet,
                    RecipeViewSet, ShoppingCartViewSet, SubscribeAPIView,
                    SubscriptionsViewSet, TagViewSet)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register(
    r'recipes/(?P<recipe_id>\d+)/favorite',
    FavoriteViewSet, basename='favorite')
router_v1.register(
    'users/subscriptions',
    SubscriptionsViewSet, basename='subscriptions')
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_cart',
    ShoppingCartViewSet, basename='shopping_cart')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/<int:author_id>/subscribe/', SubscribeAPIView.as_view()),
    path('recipes/download_shopping_cart/', DownloadShoppingCart.as_view()),
]
