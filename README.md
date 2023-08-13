# Проект Foodgram
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)



kirkir Cooking Book реализован для публикации рецептов. Авторизованные пользователи
могут подписываться на понравившихся авторов, добавлять рецепты в избранное,
в покупки, скачать список покупок ингредиентов для добавленных в покупки
рецептов.

## Подготовка и запуск проекта
### Склонировать репозиторий на локальную машину:
```
git clone git@github.com:PashkaVRN/foodgram-project-react.git
```

***- Установите и активируйте виртуальное окружение:***
- для MacOS
```
python3 -m venv venv
```
- для Windows
```
python -m venv venv
source venv/bin/activate
source venv/Scripts/activate
```

***- Установите зависимости из файла requirements.txt:***
```
pip install -r requirements.txt
```

***- Примените миграции:***
```
python manage.py migrate
```

***- В папке с файлом manage.py выполните команду для запуска локально:***
```
python manage.py runserver
```
***- Локально Документация доступна по адресу:***
```
http://127.0.0.1/api/docs/
```

### Собираем контейнерыы:

Из папки infra/ разверните контейнеры при помощи docker-compose:
```
docker-compose up -d --build
```
Выполните миграции:
```
docker-compose exec backend python manage.py migrate
```
Создайте суперпользователя:
```
winpty docker-compose exec backend python manage.py createsuperuser
```
Соберите статику:
```
docker-compose exec backend python manage.py collectstatic --no-input
```
Наполните базу данных ингредиентами и тегами. Выполняйте команду из дериктории где находится файл manage.py:
```
docker-compose exec backend python manage.py import_csv_data

```
Остановка проекта:
```
docker-compose down
```

### Подготовка к запуску проекта на удаленном сервере

Cоздать и заполнить .env файл в директории infra
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
TOKEN=252132607137
ALLOWED_HOSTS=*
```

### Примеры запросов:

**`POST` | Создание рецепта: `http://127.0.0.1:8000/api/recipes/`**

Request:
```
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```
Response:
```
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}
```

**`POST` | Подписаться на пользователя: `http://127.0.0.1:8000/api/users/{id}/subscribe/`**

Response:
```
{
  "email": "user@example.com",
  "id": 0,
  "username": "string",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "is_subscribed": true,
  "recipes": [
    {
      "id": 0,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "cooking_time": 1
    }
  ],
  "recipes_count": 0
}
```