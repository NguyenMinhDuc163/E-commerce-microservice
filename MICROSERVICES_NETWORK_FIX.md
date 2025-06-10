# Microservices Network Configuration Fixes

## Vấn đề đã giải quyết

Tất cả các microservices gặp lỗi connection khi cố gắng giao tiếp với nhau do sử dụng:
- `host.docker.internal` (không hoạt động trên tất cả môi trường)
- `localhost` và `127.0.0.1` (chỉ hoạt động trong development)

## Các thay đổi đã thực hiện

### 1. Search Service
**File**: `search_service/search_service/settings.py`
- ✅ Thay đổi từ `host.docker.internal:8001` → `product-service-container:8000`

**File**: `search_service/search/views.py`  
- ✅ Thêm error handling và timeout cho requests
- ✅ Xử lý ConnectionError, Timeout exceptions riêng biệt

### 2. Shipment Service
**File**: `shipment_service/ship_status/views.py`
- ✅ `127.0.0.1:8002` → `user-service-container:8000`
- ✅ `127.0.0.1:8005` → `order-service-container:8000`  
- ✅ `localhost:8002` → `user-service-container:8000`

### 3. Payment Service
**File**: `payment_service/payment/views.py`
- ✅ `127.0.0.1:8002` → `user-service-container:8000`
- ✅ `127.0.0.1:8005` → `order-service-container:8000`
- ✅ `127.0.0.1:8006` → `shipment-service-container:8000`

### 4. Order Service  
**File**: `order_service/order/views.py`
- ✅ `host.docker.internal:8002` → `user-service-container:8000`
- ✅ `host.docker.internal:8001` → `product-service-container:8000`
- ✅ `host.docker.internal:8006` → `shipment-service-container:8000`
- ✅ `host.docker.internal:8007` → `payment-service-container:8000`

### 5. Cart Service
**File**: `cart_service/cart/views.py`  
- ✅ `host.docker.internal:8002` → `user-service-container:8000`

### 6. Docker Compose Dependencies
**File**: `docker-compose.yml`
- ✅ Thêm `depends_on` để đảm bảo services start theo đúng thứ tự
- ✅ Cập nhật environment variables với container names
- ✅ Đảm bảo search_service start sau product_service

## Mapping Container Names và Ports

| Service | Container Name | Internal Port | External Port |
|---------|---------------|---------------|---------------|
| User Service | `user-service-container` | 8000 | 8002 |
| Product Service | `product-service-container` | 8000 | 8001 |
| Cart Service | `cart-service-container` | 8000 | 8003 |
| Search Service | `search-service-container` | 8000 | 8004 |
| Order Service | `order-service-container` | 8000 | 8005 |
| Shipment Service | `shipment-service-container` | 8000 | 8006 |
| Payment Service | `payment-service-container` | 8000 | 8007 |
| Review Service | `review-service-container` | 8000 | 8008 |

## Dependencies Graph

```
user_service (base)
├── cart_service → user_service
├── search_service → product_service
├── order_service → user_service, product_service
├── shipment_service → user_service, order_service  
└── payment_service → user_service, order_service, shipment_service
```

## Cách restart để áp dụng thay đổi

```bash
# Option 1: Restart từng service
docker-compose down search_service shipment_service payment_service order_service cart_service
docker-compose up --build -d search_service shipment_service payment_service order_service cart_service

# Option 2: Restart toàn bộ stack (khuyến nghị)
docker-compose down
docker-compose up --build -d
```

## Test các services

Sau khi restart, test các APIs:

```bash
# Test search service
curl "http://localhost:8004/api/search_service/search_books/" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Test shipment service  
curl "http://localhost:8006/api/shipment_service/create/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"order_item_id": 1, "user_id": 1}'

# Test payment service
curl "http://localhost:8007/api/payment_service/create/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"order_item_id": 1, "payment_type": "CREDIT_CARD"}'
```

## Lợi ích của giải pháp

1. **Reliability**: Sử dụng Docker internal networking thay vì external networking
2. **Performance**: Giảm latency khi giao tiếp giữa containers  
3. **Security**: Traffic không đi qua host network
4. **Scalability**: Dễ dàng scale và deploy trên các môi trường khác nhau
5. **Error Handling**: Proper timeout và exception handling

## Lưu ý

- Tất cả inter-service communication giờ sử dụng container names và port 8000 (internal)
- External APIs vẫn sử dụng ports 8001-8008 như cũ
- Dependencies được định nghĩa rõ ràng trong docker-compose.yml 