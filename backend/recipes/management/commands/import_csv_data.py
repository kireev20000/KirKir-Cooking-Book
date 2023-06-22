"""Кастомная management-команда для импорта csv файлов."""

import csv

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from recipes.models import Ingredient


class Command(BaseCommand):
    """Кастомная management-команда для импорта csv файлов."""

    def handle(self, *args, **options):

        answer = input('Вы хотите импортировать 2000 ингредиентов. Продолжить? (y/n)')
        if answer == 'n':
            self.stdout.write('Скрипт прерван.')
            quit()

        with open(f'{settings.BASE_DIR}/data/ingredients.csv',
                  'r', encoding='utf-8') as f:
            cvs_rows = csv.reader(f, delimiter=',')
            count_new, count_old = 0, 0
            for row in cvs_rows:
                name, unit = row
                print(name, unit)

                if Ingredient.objects.filter(name=name, measurement_unit=unit).exists():
                    count_old += 1
                    continue
                try:
                    Ingredient.objects.create(name=name, measurement_unit=unit)
                    count_new += 1
                except IntegrityError as e:
                    raise CommandError(
                        f'Ошибка: {e}, строка {row}'
                    )
        self.stdout.write(f'Таблица импортирована! Новых {count_new}, пропущено дубликатов {count_old}')



