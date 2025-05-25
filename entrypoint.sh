#!/bin/bash

# Запускаем сервер в фоне
python manage.py runserver 0.0.0.0:8000 &

sleep 3

# Запускаем бота
python manage.py startbot
