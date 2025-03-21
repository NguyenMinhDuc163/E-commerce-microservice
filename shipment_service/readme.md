 docker build -t shipment_service .
 
docker run -p 8007:8000 -e DATABASE_HOST=host.docker.internal -e DATABASE_NAME=mydb -e DATABASE_USER=postgres -e DATABASE_PASSWORD=NguyenDuc@163 shipment_service