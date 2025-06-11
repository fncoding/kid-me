# Getting Started

A quick guide to a dev version of my project to inspect the code :)

## Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your system
- [Python](https://www.python.org/downloads/) (if you want to use the virtual environment locally)

## Setup Instructions

1. **Copy Environment Variables**

    Copy the example environment file to create your own configuration:
    ```sh
    cp src/.env.example src/.env.dev
    ```

2. **Create Python Virtual Environment (Optional)**

    If you want to run the project locally (outside Docker), create a virtual environment:

    windows:
    ```sh
    cd src && py -m venv venv
    ```
     linux:
    ```sh
    cd src && python3 -m venv venv
    ```
3. **Build and Start Docker Containers**

     on windows:
    ```sh
    .\venv\Scripts\activate
    ```
     on linux:
    ```sh
    source venv/bin/activate
    ```
    Install requirements
    in (venv) :
    ```sh
    pip install -r requirements.txt
    ```
    
4. **Build and Start Docker Containers**

    Build the Docker images and start the containers:
    ```sh
    docker-compose up --build
    ```

4. **[VERY IMPORTANT] Apply Database Migrations**

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

- settings.py for prod - check lines for comments

---

