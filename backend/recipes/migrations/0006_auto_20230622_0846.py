# Generated by Django 3.2.16 on 2023-06-22 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_alter_favorite_recipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='Слаг'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('recipe', 'recipe_subscriber'), name='unique_recipe_subscriber_recipe'),
        ),
    ]
