# 🚗 Car Showroom Telegram Bot @TestCarShowroomBot

Проект на Django + Aiogram 3: Telegram-бот для аренды автомобилей с административной панелью.

## 📦 Возможности

- Просмотр категорий и марок автомобилей
- Пагинация и детальное описание авто
- Добавление автомобилей в корзину
- Формирование заказа
- Админ-панель Django:
  - Управление автомобилями, категориями, брендами
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

2. Создать .env файл рядом с settings.py:
    DB_NAME=
    DB_USER=
    DB_PASSWORD=
    DB_HOST=
    DB_PORT=

3. Установить зависимости:
    pip install -r requirements.txt

4. Выполнить миграции и запустить сервер:
    python manage.py migrate
    python manage.py runserver

5. Запуск Telegram-бота:
    python manage.py startbot



