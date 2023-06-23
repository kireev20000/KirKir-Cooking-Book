# Generated by Django 3.2.16 on 2023-06-19 23:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20230620_0605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_favorite', to='recipes.recipe', verbose_name='Рецепт'),
        ),
    ]