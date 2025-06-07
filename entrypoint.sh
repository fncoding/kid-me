#!/bin/sh
set -e

# Wechsel ins app-Verzeichnis
cd /app

# Die settings.py wird basierend auf DEBUG entscheiden, welche DB verwendet wird.
# Wir stellen sicher, dass die Umgebungsvariablen (DEBUG, DATABASE_URL,
# POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB) korrekt gesetzt sind,
# damit Django die richtige Datenbank für Migrationen auswählt.

echo "Waiting for DB to be ready for migrations..."
# In einer robusten Produktionsumgebung oder bei langsamen DB-Starts
# könnte hier ein Skript wie wait-for-it.sh nützlich sein.

MIGRATED=false
for i in 1 2 3 4 5; do
  if python manage.py migrate --noinput; then
    echo "Migrations successful."
    MIGRATED=true
    break
  else
    echo "Migration failed (attempt $i/5), retrying in 5s..."
    sleep 5
  fi
done

if [ "$MIGRATED" = "false" ]; then
  echo "Migrations failed after multiple attempts. Exiting."
  exit 1
fi

# Führe den CMD aus dem Dockerfile aus (z.B. Gunicorn oder Django Development Server)
exec "$@"