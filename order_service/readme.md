docker build -t order_service .

docker run -p 8005:8000 \
  -e DATABASE_HOST=host.docker.internal \
  -e DATABASE_NAME=mydb \
  -e DATABASE_USER=postgres \
  -e DATABASE_PASSWORD=NguyenDuc@163 \
  order_service

docker run -p 8005:8000 -e DATABASE_HOST=host.docker.internal -e DATABASE_NAME=mydb -e DATABASE_USER=postgres -e DATABASE_PASSWORD=NguyenDuc@163 order_service

docker run -p 8005:8000 --add-host=host.docker.internal:host-gateway -e DATABASE_HOST=host.docker.internal -e DATABASE_PORT=5433 -e DATABASE_NAME=mydb -e DATABASE_USER=postgres -e DATABASE_PASSWORD=NguyenDuc@163 order_service