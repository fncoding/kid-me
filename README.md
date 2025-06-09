
docker-compose up --build

docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser # Falls du einen Admin-User brauchst

