#!/bin/bash

echo "Waiting for postgres..."

for i in {1..30}
do
  nc -z db 5432 && echo "Postgres is up!" && break
  echo "Waiting for postgres to be ready... ($i)"
  sleep 1
done

# Запускаем сервер
python manage.py runserver 0.0.0.0:8000
