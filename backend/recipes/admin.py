from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientForRecipe, Recipe,
                     ShoppingCart, Tag)
from users.models import User

admin.site.unregister(User)


class UserFavoriteInline(admin.TabularInline):
    model = Favorite
    extra = 0


class UserRecipeInline(admin.TabularInline):
    model = Recipe
    extra = 0
    readonly_fields = ('pub_date', )
    fields = ('name', 'pub_date', )


class UserAdmin(admin.ModelAdmin):
    inlines = (UserRecipeInline, UserFavoriteInline, )
    list_display = ('username', 'email', 'is_superuser')
    search_fields = ('username', 'email')
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
        'color',
    )
    prepopulated_fields = {'slug': ('name',)}
    list_display_links = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    search_fields = ('name',)
    list_display_links = ('name',)
    empty_value_display = '-пусто-'


class RecipeIngredientInline(admin.TabularInline):
    model = IngredientForRecipe
    extra = 2


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline, )
    readonly_fields = ('in_favorites_count',)
    list_display = (
        'id',
        'name',
        'author'
    )
    list_display_links = ('name', )
    search_fields = ('name', )
    raw_id_fields = ('author', )
    list_filter = ('author', 'tags', )
    empty_value_display = '-пусто-'

    def in_favorites_count(self, obj):
        return obj.in_favorite.count()

    in_favorites_count.short_description = 'Добавлений в избранное:'


@admin.register(Favorite)
class Favorite(admin.ModelAdmin):
    list_display = ('recipe', 'recipe_subscriber', )
    list_filter = ('recipe_subscriber',)
    raw_id_fields = ('recipe_subscriber',)
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCart(admin.ModelAdmin):
    list_display = ('cart_owner', 'recipe', )
    list_filter = ('cart_owner',)
    raw_id_fields = ('cart_owner',)
    empty_value_display = '-пусто-'
