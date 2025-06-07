FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Wenn sich workspace im src-Ordner befindet:
ENV PYTHONPATH=/app/src


CMD ["python", "manage.py", "makemigrations","&&", "gunicorn", "--bind", "0.0.0.0:8000", "workspace.wsgi:application"]