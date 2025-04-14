#!/bin/sh

echo "Waiting for database..."
while ! nc -z "$DATABASE_HOST" "$DATABASE_PORT"; do
  sleep 2
done
echo "Database is ready!"

python manage.py migrate --noinput

exec gunicorn zaiko_be.wsgi:application \
    -w 4 \
    -b 0.0.0.0:8000 
