docker build -t user_service .

docker run  -p 8008:8000 -e DATABASE_HOST=host.docker.internal -e DATABASE_NAME=user_service -e DATABASE_USER=root -e DATABASE_PASSWORD=NguyenDuc@163 user_service


docker tag cart_service:latest cart_service:v1.0.0
docker tag order_service:latest order_service:v1.0.0
docker tag payment_service:latest payment_service:v1.0.0
docker tag product_service:latest product_service:v1.0.0
docker tag review_service:latest review_service:v1.0.0
docker tag search_service:latest search_service:v1.0.0
docker tag shipment_service:latest shipment_service:v1.0.0
docker tag user_service:latest user_service:v1.0.0

docker tag cart_service:v1.0.0 nguyenduc1603/cart_service:v1.0.0

docker pull nguyenduc1603/cart_service:v1.0.0
docker pull nguyenduc1603/order_service:v1.0.0
docker pull nguyenduc1603/payment_service:v1.0.0
docker pull nguyenduc1603/product_service:v1.0.0
docker pull nguyenduc1603/review_service:v1.0.0
docker pull nguyenduc1603/search_service:v1.0.0
docker pull nguyenduc1603/shipment_service:v1.0.0
docker pull nguyenduc1603/user_service:v1.0.0