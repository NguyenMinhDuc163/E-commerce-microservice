docker build -t payment-service-image .

docker run -p 8003:8000 -e DATABASE_HOST=host.docker.internal -e DATABASE_NAME=mydb -e DATABASE_USER=postgres -e DATABASE_PASSWORD=NguyenDuc@163 payment_service