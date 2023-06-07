## Workflow status

![Workflow status badge](https://github.com/bvsvrvb/foodgram-project-react/actions/workflows/main.yml/badge.svg)

## Ссылка на развёрнутый проект

http://51.250.76.39/

### Данные для входа в админ-панель

Логин: ```admin```

Пароль: ```Adm1n000```

# Foodgram - Продуктовый помощник

Foodgram - сайт, где пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список избранное, а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Список Backend-технологий

- Python
- Django
- Django Rest Framework
- Djoser
- PostgreSQL
- Gunicorn
- Nginx
- Docker
- Docker-compose

## Локальный запуск проекта

Склонировать репозиторий:

```
git clone https://github.com/bvsvrvb/foodgram-project-react.git
```

В директории infra/ создать файл .env и добавить переменные окружения:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
DB_HOST=db
DB_PORT=5432
```

Создать и запустить контейнеры Docker (находясь в infra/):

```
sudo docker-compose up
```

Выполнить миграции:

```
sudo docker-compose exec backend python manage.py migrate
```

Собрать статику:

```
sudo docker-compose exec backend python manage.py collectstatic --noinput
```

Создать суперпользователя:

```
sudo docker-compose exec backend python manage.py createsuperuser
```

Заполнить БД ингредиентами и тегами:

```
sudo docker-compose exec backend python manage.py load_data_ingredients
```
```
sudo docker-compose exec backend python manage.py load_data_tags
```
