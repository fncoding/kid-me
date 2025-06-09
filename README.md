# Project Setup Guide

This guide will help you set up and run the project locally using Docker and Python virtual environments.

## Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your system
- [Python](https://www.python.org/downloads/) (if you want to use the virtual environment locally)

## Setup Instructions

1. **Copy Environment Variables**

    Copy the example environment file to create your own configuration:
    ```sh
    cp .env.example .env
    ```

2. **Create Python Virtual Environment (Optional)**

    If you want to run the project locally (outside Docker), create a virtual environment:
    ```sh
    cd src && py -m venv venv
    ```

3. **Build and Start Docker Containers**

    Build the Docker images and start the containers:
    ```sh
    docker-compose up --build
    ```

4. **Apply Database Migrations**

    Run database migrations inside the Docker container:
    ```sh
    docker-compose exec web python manage.py migrate
    ```

5. **Create Superuser (Optional)**

    If you need an admin user, create a superuser:
    ```sh
    docker-compose exec web python manage.py createsuperuser
    ```

## Notes

- Make sure to configure your `.env` file with the appropriate settings for your environment.
- For development, you can use the provided Docker setup to ensure consistency across different systems.

---
cp .env.example .env
cd src && py -m venv venv

docker-compose up --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser # Falls du einen Admin-User brauchst

