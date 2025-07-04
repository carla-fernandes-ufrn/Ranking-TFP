#!/usr/bin/env bash

# Roda as migrações
python manage.py makemigrations
python manage.py migrate

# Cria o superuser se não existir
echo "from django.contrib.auth import get_user_model; \
User = get_user_model(); \
User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists() or \
User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')" | python manage.py shell

# Coleta arquivos estáticos
python manage.py collectstatic --noinput

# Inicia o servidor
gunicorn Ranking.wsgi:application
