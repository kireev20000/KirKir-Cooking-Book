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

        model = kwargs.get('model')
        args = {
            'recipe': self.kwargs.get('recipe_id'),
             kwargs.get('fkey'): self.request.user
        }

        if not model.objects.filter(**args):
            return Response(
                {'errors': 'Рецепт не добавлен в список!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        instance = get_object_or_404(model, **args)
        instance_name = instance.recipe.name
        self.perform_destroy(instance)
        return Response(
            {'success': f'Рецепт {instance_name} удален из вашего списка!'},
            status=status.HTTP_204_NO_CONTENT,
        )

    def perform_destroy(self, instance):
        instance.delete()
