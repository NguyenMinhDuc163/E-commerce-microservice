docker build -t payment_service .

docker run -p 8007:8000 -e DATABASE_HOST=host.docker.internal -e DATABASE_NAME=mydb -e DATABASE_USER=postgres -e DATABASE_PASSWORD=YOUR_POSTGRES_PASSWORD_HERE payment_service