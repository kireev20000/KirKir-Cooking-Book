from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from recipes.models import (
    Favorite,
    Ingredient,
    IngredientForRecipe,
    Recipe,
    ShoppingCart,
    Tag
)
from users.models import User
from users.serializers import RecipeShortListSerializer

from .mixins import ReadOnlyMixin


class TagSerializer(ReadOnlyMixin, serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(ReadOnlyMixin, serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientForRecipeSerializer(ReadOnlyMixin,
                                    serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id', )
    name = serializers.ReadOnlyField(source='ingredient.name', )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = IngredientForRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class FavoriteRecipeSerializer(ReadOnlyMixin, serializers.ModelSerializer):

    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = serializers.CharField(source='recipe.image', read_only=True)
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = Favorite
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )

    def validate(self, data):
        user = self.context.get('request').user
        recipe_id = self.context.get('recipe_id')

        if Favorite.objects.filter(
                recipe_subscriber=user,
                recipe=recipe_id
        ).exists():
            raise ValidationError(
                {'errors': 'Этот рецепт уже в вашем избранном!'}
            )
        return data


class UserSerializer(serializers.ModelSerializer):

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return user.follower.filter(author=obj.id).exists()


class RecipeCRUDSerializer(serializers.ModelSerializer):

    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True, many=False)
    ingredients = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField(allow_empty_file=False)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and Favorite.objects.filter(
                recipe=obj,
                recipe_subscriber=user,
            ).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and ShoppingCart.objects.filter(
                recipe=obj,
                cart_owner=user,
            ).exists()
        )

    @staticmethod
    def get_ingredients(recipe):
        queryset = IngredientForRecipe.objects.filter(recipe=recipe)
        serializer = IngredientForRecipeSerializer(queryset, many=True)
        return serializer.data

    @staticmethod
    def add_ingredients(new_recipe, ingredients):
        IngredientForRecipe.objects.bulk_create(
            IngredientForRecipe(
                recipe=new_recipe,
                ingredient=get_object_or_404(
                    Ingredient, id=ingredient.get('id')
                ), amount=ingredient.get('amount')
            )
            for ingredient in ingredients)
        return new_recipe

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = self.initial_data.get('tags')
        ingredients = self.initial_data.get('ingredients')
        for ingredient in ingredients:
            if not str(ingredient.get('amount')).isdigit():
                raise ValidationError('errors: Количество должно быть числом!')
        new_recipe = Recipe.objects.create(author=author, **validated_data)
        new_recipe.tags.set(tags)
        return self.add_ingredients(new_recipe, ingredients)

    def update(self, instance, validated_data):
        instance.tags.clear()
        IngredientForRecipe.objects.filter(recipe=instance).delete()
        instance.tags.set(self.initial_data.get('tags'))
        ingredients = self.initial_data.get('ingredients')
        for ingredient in ingredients:
            if not str(ingredient.get('amount')).isdigit():
                raise ValidationError('errors: Количество должно быть числом!')
        self.add_ingredients(instance, ingredients)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ShoppingCartSerializer(ReadOnlyMixin, serializers.ModelSerializer):

    class Meta:
        model = ShoppingCart
        fields = ('cart_owner', 'recipe')

    def to_representation(self, instance):
        return RecipeShortListSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data

    def validate(self, data):
        cart_owner = self.context.get('request').user
        recipe = self.context.get('recipe')
        data['recipe'] = recipe
        data['cart_owner'] = cart_owner
        if ShoppingCart.objects.filter(cart_owner=cart_owner,
                                       recipe=recipe):
            raise ValidationError(
                {'errors': f'Рецепт {recipe.name} уже в вашей корзине!'}
            )
        return data
