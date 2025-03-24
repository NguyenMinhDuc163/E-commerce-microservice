FROM python:3.10-slim

# Thiết lập biến môi trường
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_DOCKER_ENV=1
# Thiết lập thư mục làm việc
WORKDIR /app

# Cài đặt các gói cần thiết cho PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt các dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào container
COPY . .

# Expose port cho Django server
EXPOSE 8000

# Tạo một script để chạy migrations và khởi động server
RUN echo '#!/bin/bash\n\
python manage.py migrate\n\
python manage.py runserver 0.0.0.0:8000' > /app/entrypoint.sh && \
chmod +x /app/entrypoint.sh

# Chạy entrypoint script
CMD ["/app/entrypoint.sh"]