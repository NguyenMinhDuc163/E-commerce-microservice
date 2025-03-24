docker build -t user_service .

docker run  -p 8008:8000 -e DATABASE_HOST=host.docker.internal -e DATABASE_NAME=user_service -e DATABASE_USER=root -e DATABASE_PASSWORD=NguyenDuc@163 user_service


