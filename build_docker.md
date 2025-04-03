# đổi tag local
docker tag cart_service:latest cart_service:v1.0.2
docker tag order_service:latest order_service:v1.0.2
docker tag payment_service:latest payment_service:v1.0.2
docker tag product_service:latest product_service:v1.0.2
docker tag review_service:latest review_service:v1.0.2
docker tag search_service:latest search_service:v1.0.2
docker tag shipment_service:latest shipment_service:v1.0.2
docker tag user_service:latest user_service:v1.0.2

# đổi tag dockerhub
docker tag cart_service:v1.0.2 nguyenduc1603/cart_service:v1.0.2
docker tag order_service:v1.0.2 nguyenduc1603/order_service:v1.0.2
docker tag payment_service:v1.0.2 nguyenduc1603/payment_service:v1.0.2
docker tag product_service:v1.0.2 nguyenduc1603/product_service:v1.0.2
docker tag review_service:v1.0.2 nguyenduc1603/review_service:v1.0.2
docker tag search_service:v1.0.2 nguyenduc1603/search_service:v1.0.2
docker tag shipment_service:v1.0.2 nguyenduc1603/shipment_service:v1.0.2
docker tag user_service:v1.0.2 nguyenduc1603/user_service:v1.0.2

# đẩy lên docker hub 
docker push nguyenduc1603/cart_service:v1.0.2
docker push nguyenduc1603/order_service:v1.0.2
docker push nguyenduc1603/payment_service:v1.0.2
docker push nguyenduc1603/product_service:v1.0.2
docker push nguyenduc1603/review_service:v1.0.2
docker push nguyenduc1603/search_service:v1.0.2
docker push nguyenduc1603/shipment_service:v1.0.2
docker push nguyenduc1603/user_service:v1.0.2

# kéo về
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


# xoa thua
docker rmi cart_service:latest
docker rmi order_service:latest
docker rmi payment_service:latest
docker rmi product_service:latest
docker rmi review_service:latest
docker rmi search_service:latest
docker rmi shipment_service:latest
docker rmi user_service:latest


#run
docker-compose up -d
