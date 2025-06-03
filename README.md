# 🚗 DGANGO_ADMIN_POSTGRE Telegram Bot @TestCarShowroomBot

Проект на Django + Aiogram 3: Telegram-бот продажи товаров с административной панелью и Базой данных PostgreSQL

## 📦 Возможности

- Просмотр категорий и подкатегорий
- Пагинация и детальное описание товара
- Добавление товара в корзину
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

2. Создать .env файл рядом с docker-compose.yml:
    SECRET_KEY=

    DB_ENGINE=
    POSTGRES_DB=
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    POSTGRES_HOST=
    POSTGRES_PORT=

    BOT_TOKEN=
    CHANNEL_ID=
    CHANNEL_NAME=

    PROVIDER_TOKEN= # Токен Юкасса
    ORDERS_FILE= # сохранения заказов в EXCEL

3. Настройки бота:
    /bot/config.py

4. Общая папка:
    shared_media/

5. выполнить из корня, где находится docker-compose.yml
    docker-compose up --build

6. В контейнере django:
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser

7. Наполняем базу данных в админке.
    
