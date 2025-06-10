docker build -t product_service .

docker run -d -p 8001:8000 -e MONGODB_URI="mongodb+srv://YOUR_MONGO_USERNAME:YOUR_MONGO_PASSWORD@your-cluster.mongodb.net/?retryWrites=true&w=majority&appName=YourAppName" -e MONGODB_DB_NAME="book_app" product_service