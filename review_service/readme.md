docker build -t review_service .

docker run -d -p 8008:8000 -v review_data:/app/data review_service