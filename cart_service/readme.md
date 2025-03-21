docker build -t cart_service .

docker run -p 8001:8000 \
  -e DATABASE_HOST=host.docker.internal \
  -e DATABASE_NAME=cart_service \
  -e DATABASE_USER=root \
  -e DATABASE_PASSWORD=NguyenDuc@163 \
  cart_service