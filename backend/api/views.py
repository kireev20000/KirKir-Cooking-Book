from datetime import datetime

from django.db.models import Sum
from django.shortcuts import HttpResponse, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipes.models import (
    Favorite,
    Ingredient,
    IngredientForRecipe,
    Recipe,
    ShoppingCart,
    Tag
)

from .filters import RecipeFilter
from .mixins import CustomListRecipeDeleteMixin
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import (
    FavoriteRecipeSerializer,
    IngredientSerializer,
    RecipeCRUDSerializer,
    ShoppingCartSerializer,
    TagSerializer
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    search_fields = ('^name',)
    ordering_fields = ('name', 'slug', )
    http_method_names = ('get', )


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (AllowAny, )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    search_fields = ('^name', )
    ordering_fields = ('name', 'measurement_unit', )
    http_method_names = ('get', )


class RecipeViewSet(viewsets.ModelViewSet):

    queryset = Recipe.objects.all()
    serializer_class = RecipeCRUDSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorOrAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter
    http_method_names = ('get', 'post', 'patch', 'delete', )


class FavoriteViewSet(mixins.CreateModelMixin,
                      CustomListRecipeDeleteMixin,
                      viewsets.GenericViewSet):

    queryset = Favorite.objects.all()
    serializer_class = FavoriteRecipeSerializer
    permission_classes = (IsAuthenticated, )
    http_method_names = ('post', 'delete', )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'recipe_id': self.kwargs.get('recipe_id')})
        return context

    def perform_create(self, serializer):
        recipe = get_object_or_404(
            Recipe,
            pk=self.kwargs.get('recipe_id'),
        )
        serializer.save(
            recipe_subscriber=self.request.user,
            recipe=recipe,
        )

    def delete(self, request, recipe_id):
        return super().destroy(
            self,
            request,
            model=Favorite,
            fkey='recipe_subscriber'
        )


class ShoppingCartViewSet(mixins.CreateModelMixin,
                          CustomListRecipeDeleteMixin,
                          viewsets.GenericViewSet):

    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticated, )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        recipe = get_object_or_404(
            Recipe,
            pk=self.kwargs.get('recipe_id')
        )
        context.update({'recipe': recipe})
        context.update({'cart_owner': self.request.user})
        return context

    def delete(self, request, recipe_id):
        return super().destroy(
            self,
            request,
            model=ShoppingCart,
            fkey='cart_owner'
        )

    @staticmethod
    def download_shopping_cart(request):
        if not ShoppingCart.objects.filter(cart_owner=request.user):
            return Response({'errors': 'Ваша корзина пуста!'},
                            status=status.HTTP_400_BAD_REQUEST)
        shopping_cart = IngredientForRecipe.objects.filter(
            recipe__shopping_cart__cart_owner=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(
            total=Sum('amount')
        )

        text = f'Список покупок на {datetime.now().strftime("%d.%m.%Y")}:\n\n'
        for ingredient in shopping_cart:
            text += (f'{ingredient["ingredient__name"]}: '
                     f'{ingredient["total"]}'
                     f'{ingredient["ingredient__measurement_unit"]}\n')

        response = HttpResponse(text, content_type='text/plain')
        filename = f'shopping_list_{datetime.now().strftime("%d.%m.%Y")}.txt'
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
