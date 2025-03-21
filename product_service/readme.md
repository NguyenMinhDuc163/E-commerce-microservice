docker build -t product_service .

docker run -d -p 8004:8000 -e MONGODB_URI="mongodb+srv://nguyenduc:bMfuLqGps59NJLI8@cluster0.ld2i8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0" -e MONGODB_DB_NAME="book_app" product_service