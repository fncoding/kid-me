# Base Image mit Python 3.11 (ältere Versionen können Probleme machen auf Render)
FROM python:3.11-slim

# Arbeitsverzeichnis setzen
WORKDIR /app

# Requirements installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Quellcode kopieren
COPY src/ .

# entrypoint.sh kopieren und ausführbar machen
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Gunicorn starten
ENTRYPOINT ["/app/entrypoint.sh"]