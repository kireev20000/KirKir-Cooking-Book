"""Эндпойнты приложения YaMDb."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (DownloadShoppingCart, FavoriteViewSet, IngredientViewSet,
                       RecipeViewSet, ShoppingCartViewSet, TagViewSet)
from users.views import SubscribeAddDelView, SubscriptionsViewSet

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
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('recipes/download_shopping_cart/', DownloadShoppingCart.as_view()),
    path('', include(router_v1.urls)),
    path('users/<int:user_id>/subscribe/', SubscribeAddDelView.as_view()),
]
