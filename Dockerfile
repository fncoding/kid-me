# Base Image mit Python 3.11 (ältere Versionen können Probleme machen auf Render)
FROM python:3.11-slim

# Arbeitsverzeichnis setzen
WORKDIR /app

# Requirements installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Quellcode kopieren
COPY src/ .

# Gunicorn starten
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "workspace.wsgi:application"]