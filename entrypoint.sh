#!/bin/sh
set -e

# Wechsel ins app-Verzeichnis (wo manage.py liegt, nachdem src/ . nach /app kopiert wurde)
cd /app

# Warte bis DB erreichbar ist (optional, wenn externe DB)
if [ "$DATABASE_URL" ]; then
  until python manage.py migrate --noinput; do
    echo "Migration failed, retrying in 2s..."
    sleep 2
  done
else
  echo "No DATABASE_URL set, skipping migrations"
fi

# Server starten
exec gunicorn --bind 0.0.0.0:8000 workspace.wsgi:application