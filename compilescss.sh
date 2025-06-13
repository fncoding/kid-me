cd src
npm run build-static:win
cd ..
docker-compose -f docker-compose.prod.yml up --build -d
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput