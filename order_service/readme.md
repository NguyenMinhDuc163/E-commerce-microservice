
docker run -p 8002:8000 \
  -e DATABASE_HOST=host.docker.internal \
  -e DATABASE_NAME=mydb \
  -e DATABASE_USER=postgres \
  -e DATABASE_PASSWORD=NguyenDuc@163 \
  order_service