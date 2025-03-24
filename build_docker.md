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


docker build -t cart_service .
docker build -t order_service .
docker build -t payment_service .
docker build -t product_service .
docker build -t review_service .
docker build -t search_service .
docker build -t shipment_service .
docker build -t user_service .