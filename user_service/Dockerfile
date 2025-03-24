FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_DOCKER_ENV=1
# Thiết lập thư mục làm việc
WORKDIR /app

# Cài đặt các dependencies
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code
COPY . .

# Xác định vị trí chính xác của manage.py
RUN find / -name manage.py

EXPOSE 8000

RUN echo '#!/bin/bash\n\
python manage.py migrate\n\
python manage.py runserver 0.0.0.0:8000' > /app/entrypoint.sh && \
chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]