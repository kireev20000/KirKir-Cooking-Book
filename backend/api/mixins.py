from django.shortcuts import get_object_or_404
from rest_framework.fields import Field
from rest_framework import mixins, status

from recipes.models import ShoppingCart, Favorite
from rest_framework.response import Response

class ReadOnlyMixin(Field):

    def __new__(cls, *args, **kwargs):
        setattr(
            cls.Meta,
            'read_only_fields',
            [f.name for f in cls.Meta.model._meta.get_fields()],
        )
        return super(ReadOnlyMixin, cls).__new__(cls, *args, **kwargs)


class CustomListRecipeDeleteMixin(mixins.DestroyModelMixin):

    def destroy(self, request, *args, **kwargs):
        recipe_id = self.kwargs.get('recipe_id')
        user = self.request.user
        model = kwargs.get('model')
        if model == ShoppingCart:
            if not ShoppingCart.objects.filter(recipe=recipe_id,
                                               cart_owner=user):
                return Response({'errors': 'Рецепт не добавлен в список покупок'},
                                status=status.HTTP_400_BAD_REQUEST)
            instance = get_object_or_404(
                ShoppingCart,
                cart_owner=user,
                recipe=recipe_id,
            )
        elif model == Favorite:
            if not Favorite.objects.filter(recipe=recipe_id,
                                           recipe_subscriber=user):
                return Response(
                    {'errors': 'У вас нет этого рецепта в избранном!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            instance = get_object_or_404(
                Favorite,
                recipe_subscriber=user,
                recipe=recipe_id
            )
        instance_name = instance.recipe.name
        self.perform_destroy(instance)
        return Response(
            {'success': f'Рецепт {instance_name} удален из вашего списка!'},
            status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
