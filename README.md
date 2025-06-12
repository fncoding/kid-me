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

2. **Install Node Dependencies & Build Static Assets**

    We use npm to build Bootstrap, Bootstrap Icons, and SCSS.  
    Run these commands **before starting Docker**:

    **On Windows:**
    ```sh
    cd src
    npm install
    npm run build-static:win
    ```

    **On Linux/macOS:**
    ```sh
    cd src
    npm install
    npm run build-static:linux
    ```

3. **Create Python Virtual Environment (Optional)**

    If you want to run the project locally (outside Docker), create a virtual environment:

    **On Windows:**
    ```sh
    cd src && py -m venv venv
    .\venv\Scripts\activate
    ```

    **On Linux/macOS:**
    ```sh
    cd src && python3 -m venv venv
    source venv/bin/activate
    ```

    Install requirements:
    ```sh
    pip install -r requirements.txt
    ```

4. **Build and Start Docker Containers**

    Build the Docker images and start the containers:
    ```sh
    docker-compose up --build
    ```

5. **[VERY IMPORTANT] Apply Database Migrations**

    Run database migrations inside the Docker container:
    ```sh
    docker-compose exec web python manage.py migrate
    ```

6. **Collect Static Files (for production or after static changes)**

    If you change static files or deploy, run:
    ```sh
    docker-compose exec web python manage.py collectstatic --noinput
    ```

7. **Create Superuser (Optional)**

    If you need an admin user, create a superuser:
    ```sh
    docker-compose exec web python manage.py createsuperuser
    ```

## Notes

- **Always run the npm static build before starting Docker** if you change frontend assets.
- `settings.py` for prod - check lines for comments.
- For local development with Docker, static files must exist in the correct folders before container start.
   ```sh
    npm run build-static:linux 
    ```
     ```sh
    docker-compose -f docker-compose.prod.yml up --build -d 
    ```
    ```sh
    docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput  
    ```
     ```sh
    docker-compose exec web python manage.py collectstatic --noinput  
    ```

---

