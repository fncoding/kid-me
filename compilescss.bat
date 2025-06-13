cd src
npm run build-static:win
cd ..
docker-compose up --build -d
docker-compose exec web python manage.py collectstatic --noinput