docker build -t user_service .

docker run  -p 8002:8000 -e DATABASE_HOST=host.docker.internal -e DATABASE_NAME=user_service -e DATABASE_USER=root -e DATABASE_PASSWORD=YOUR_MYSQL_PASSWORD_HERE user_service


python manage.py runserver 8002

python manage.py migrate

python manage.py makemigrations

docker run -p 8002:8000 --add-host=host.docker.internal:host-gateway -e DATABASE_HOST=host.docker.internal -e DATABASE_PORT=3307 -e DATABASE_NAME=user_service -e DATABASE_USER=root -e DATABASE_PASSWORD=YOUR_MYSQL_PASSWORD_HERE user_service