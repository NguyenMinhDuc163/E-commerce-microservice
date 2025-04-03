docker build -t search_service .

docker run -p 8004:8000 -v search_data:/app/data search_service