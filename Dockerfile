# Stage 1: Build stage (optional, but good for managing dependencies)
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies for psycopg2 if needed (psycopg2-binary usually handles this)
# RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev

COPY src/requirements.txt .

# Create a virtual environment
RUN python -m venv /opt/venv
# Activate virtual environment and install requirements
RUN . /opt/venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Stage 2: Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./src /app/

# User for running the application (optional, but good practice)
# RUN addgroup --system app && adduser --system --group app
# USER app

EXPOSE 8000