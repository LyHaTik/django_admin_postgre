# 🚗 Car Showroom Telegram Bot @TestCarShowroomBot

Проект на Django + Aiogram 3: Telegram-бот для онлайн магазина с административной панелью.

## 📦 Возможности

- Просмотр категорий и подкатегорий товаров
- Пагинация и детальное описание
- Добавление товаров в корзину
- Формирование заказа
- Админ-панель Django:
  - Управление товарами, категориями, подкатегориями
  - Пользователи и корзины
  - Рассылка сообщений по Telegram

## 🛠️ Технологии

- Python 3.10+
- Django 4+
- PostgreSQL
- Aiogram 3

## ⚙️ Установка

1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/LyHaTik/django_admin_postgre.git
   cd car_showroom_bot

2. Создать .env файл рядом с README.md:
    SECRET_KEY=

    POSTGRES_DB=
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    POSTGRES_HOST=
    POSTGRES_PORT=

    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=
    DB_USER=
    DB_PASSWORD=
    DB_HOST=
    DB_PORT=

    BOT_TOKEN=
    CHANNEL_ID=         # ID канала
    CHANNEL_NAME=       # Имя канала

    PROVIDER_TOKEN =    # Юкасса
    ORDERS_FILE =       # имя файла .xlsx для сохранения заказа

3. Установить зависимости:
    pip install -r requirements.txt

4. Выполнить миграции, создать администратора и запустить сервер:
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

5. Запуск Telegram-бота:
    python manage.py startbot

6. Наполни админку(127.0.0.1:8000) товаром


## ⚙️ Запуск в Docker контейнере

1. ~

2. ~

3. Собрать:
    ```bash
    docker-compose up --build

4. Зайти в контейнер:
    ```bash
    docker-compose exec bot-adminpanel sh

5. Выполнить миграции, создать администратора:
    python manage.py migrate
    python manage.py createsuperuser

6. ~