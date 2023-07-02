# Foodgram - Продуктовый помощник
![Workflow status badge](https://github.com/bvsvrvb/foodgram-project-react/actions/workflows/main.yml/badge.svg)

Учебный проект Яндекс Практикум (курс Python-разработчик).

## Описание
Foodgram - сайт, где пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список избранное, а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

В рамках проекта реализован бэкенд сайта, его контейнеризация в Docker и развертывание на облачном сервере через GitHub Actions (CI/CD).

## Технологии
[![Python](https://img.shields.io/badge/Python-3.7-3776AB?logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-3.2-092E20?&logo=django)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-grey?logo=postgresql)](https://www.postgresql.org/)
[![Django REST Framework](https://img.shields.io/badge/Django_REST_Framework-grey?logo=django)](https://www.django-rest-framework.org/)
[![Gunicorn](https://img.shields.io/badge/Gunicorn-grey?logo=gunicorn)](https://gunicorn.org/)
[![nginx](https://img.shields.io/badge/nginx-grey?logo=nginx)](https://nginx.org/)
[![Docker](https://img.shields.io/badge/Docker-grey?logo=docker)](https://www.docker.com/)
[![Docker Compose](https://img.shields.io/badge/Docker_Compose-grey?logo=docker)](https://docs.docker.com/compose/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-grey?logo=githubactions)](https://github.com/features/actions)


## Запуск проекта в Docker-контейнерах
Клонировать репозиторий и перейти в директорию `infra/`:
```bash
git clone https://github.com/bvsvrvb/praktikum-foodgram.git
```
```bash
cd infra
```

Создать `.env` файл с переменными окружения:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<имя базы данных postgres>
DB_USER=<пользователь бд>
DB_PASSWORD=<пароль>
DB_HOST=db
DB_PORT=5432
```

Собрать и запустить контейнеры:
```bash
sudo docker-compose up
```

Выполнить миграции внутри контейнера `backend`:
```bash
sudo docker-compose exec backend python manage.py migrate
```

Собрать статику проекта внутри контейнера `backend`:
```bash
sudo docker-compose exec backend python manage.py collectstatic --noinput
```

Создать суперпользователя для админ-панели внутри контейнера `backend`:
```bash
sudo docker-compose exec backend python manage.py createsuperuser
```

Заполнить БД ингредиентами и тегами внутри контейнера `backend`:
```bash
sudo docker-compose exec backend python manage.py load_data_ingredients
```
```bash
sudo docker-compose exec backend python manage.py load_data_tags
```

## CI/CD GitHub Actions

### Workflow состоит из четырёх шагов:

   1. Проверка кода тестами.
   2. Сборка и публикация образа на DockerHub.
   3. Автоматический деплой и запуск контейнеров на удаленном сервере.
   4. Отправка уведомления в телеграм-чат.

### Для работы с Workflow GitHub Actions необходимо добавить в GitHub Secrets переменные окружения:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<имя базы данных postgres>
DB_USER=<пользователь бд>
DB_PASSWORD=<пароль>
DB_HOST=db
DB_PORT=5432

DOCKER_PASSWORD=<пароль от DockerHub>
DOCKER_USERNAME=<имя пользователя>

USER=<username для подключения к серверу>
HOST=<IP сервера>
PASSPHRASE=<пароль для сервера, если он установлен>
SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>

TELEGRAM_TO=<ID чата, в который придет сообщение>
TELEGRAM_TOKEN=<токен вашего бота>
```

### И подготовить удаленный сервер:
Выполнить вход на удаленный сервер:
```bash
ssh <username>@<host>
```

Установить Docker на сервере:
```bash
sudo apt install docker.io 
```

Установить Docker Compose на сервере:
```bash
sudo apt install docker-compose
```

Скопировать файлы `docker-compose.yaml` и `default.conf` на сервер:
```bash
scp docker-compose.yaml <username>@<host>:/home/<username>/
scp default.conf <username>@<host>:/home/<username>/
```
