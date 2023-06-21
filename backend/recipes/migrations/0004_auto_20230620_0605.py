# Generated by Django 3.2.16 on 2023-06-19 23:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0003_alter_favorite_recipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingcart',
            name='cart_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart', to=settings.AUTH_USER_MODEL, verbose_name='Хозяин корзины'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart', to='recipes.recipe', verbose_name='Рецепт'),
        ),
    ]
