# 🛒 Hệ Thống E-Commerce Microservices


## 📋 Tổng Quan

Đây là bài tập lớn môn **Kiến trúc và Thiết kế Phần mềm** được thiết kế theo kiến trúc microservices. Hệ thống mô phỏng một nền tảng thương mại điện tử hoàn chỉnh với các dịch vụ độc lập, có thể mở rộng và bảo trì dễ dàng.

## 🏗️ Kiến Trúc Hệ Thống

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Service  │    │ Product Service │    │ Search Service  │
│     :8002       │    │     :8001       │    │     :8004       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Cart Service   │    │ Order Service   │    │ Review Service  │
│     :8003       │    │     :8005       │    │     :8008       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
       ┌─────────────────┐    ┌─────────────────┐
       │Shipment Service │    │Payment Service  │
       │     :8006       │    │     :8007       │
       └─────────────────┘    └─────────────────┘
```

## 🔧 Danh Sách Microservices

| Service | Port | Chức Năng | Mô Tả |
|---------|------|-----------|-------|
| **User Service** | 8002 | Quản lý người dùng | Đăng ký, đăng nhập, profile, xác thực |
| **Product Service** | 8001 | Quản lý sản phẩm | CRUD sản phẩm, danh mục, kho hàng |
| **Cart Service** | 8003 | Giỏ hàng | Thêm/xóa sản phẩm, tính toán tổng tiền |
| **Search Service** | 8004 | Tìm kiếm | Tìm kiếm sản phẩm, filter, sort |
| **Order Service** | 8005 | Quản lý đơn hàng | Tạo đơn, theo dõi trạng thái, lịch sử |
| **Shipment Service** | 8006 | Vận chuyển | Quản lý giao hàng, tracking |
| **Payment Service** | 8007 | Thanh toán | Xử lý thanh toán, refund |
| **Review Service** | 8008 | Đánh giá | Đánh giá sản phẩm, rating |

## ⚠️ **QUAN TRỌNG - BẢO MẬT**

**Trước khi sử dụng, BẮT BUỘC phải thay đổi các thông tin sau:**

### 🔐 Mật khẩu cần thay đổi:
- `YOUR_MYSQL_PASSWORD_HERE` → Mật khẩu MySQL thực tế
- `YOUR_POSTGRES_PASSWORD_HERE` → Mật khẩu PostgreSQL thực tế  
- `YOUR_MONGO_USERNAME` và `YOUR_MONGO_PASSWORD` → Thông tin MongoDB thực tế

### 🔑 Secret Keys cần thay đổi:
Tất cả các `YOUR_DJANGO_SECRET_KEY_HERE_*` trong các file settings.py

**Cách tạo Secret Key mới:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 📁 Các file cần chỉnh sửa:
- `user_service/user_service/settings.py`
- `cart_service/cart_service/settings.py`
- `order_service/order_service/settings.py`
- `payment_service/payment_service/settings.py`
- `shipment_service/shipment_service/settings.py`
- `product_service/product_service/settings.py`
- `review_service/review_service/settings.py`
- `search_service/search_service/settings.py`
- `docker-compose.yml`

## 🚀 Hướng Dẫn Cài Đặt

### Yêu Cầu Hệ Thống
- **Python**: 3.8 hoặc cao hơn
- **Django**: 3.1+
- **Database**: MySQL, PostgreSQL, MongoDB
- **Docker**: Để chạy toàn bộ hệ thống
- **IDE**: PyCharm, VS Code

### Cài Đặt và Chạy

1. **Clone repository**
   ```bash
   git clone [repository-url]
   cd Software_Architecture_and_Design_PTIT
   ```

2. **Cài đặt dependencies**
   ```bash
   # Tạo virtual environment
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # hoặc
   .venv\Scripts\activate     # Windows
   
   # Cài đặt dependencies cho từng service
   cd user_service && pip install -r requirements.txt
   cd ../product_service && pip install -r requirements.txt
   # ... tương tự cho các service khác
   ```

3. **Cấu hình database**
   - MySQL cho User Service và Cart Service
   - PostgreSQL cho Order, Payment, Shipment Services
   - MongoDB cho Product Service
   - File-based storage cho Review và Search Services

4. **Chạy bằng Docker (Khuyến nghị)**
   ```bash
   # Chạy toàn bộ hệ thống
   docker-compose up -d
   
   # Kiểm tra logs
   docker-compose logs -f
   ```

5. **Chạy từng service riêng lẻ**
   ```bash
   # Chạy từng service
   cd user_service
   python manage.py runserver 8002
   
   cd ../product_service
   python manage.py runserver 8001
   # ... tương tự cho các service khác
   ```

## 📡 API Documentation

### 🛍️ Order Service (Port: 8005)

| Endpoint | Method | Mô Tả |
|----------|--------|-------|
| `/api/order/all` | GET | Lấy danh sách tất cả đơn hàng |
| `/api/order/all/status/{status}` | GET | Lấy đơn hàng theo trạng thái |
| `/api/order/add` | POST | Tạo đơn hàng mới |
| `/api/order/detail/{id}` | GET | Chi tiết đơn hàng |

### 📦 Product Service (Port: 8001)
```
GET    /api/products          - Danh sách sản phẩm
GET    /api/products/{id}     - Chi tiết sản phẩm
POST   /api/products          - Tạo sản phẩm mới
PUT    /api/products/{id}     - Cập nhật sản phẩm
DELETE /api/products/{id}     - Xóa sản phẩm
```

### 👤 User Service (Port: 8002)
```
POST   /api/users/register    - Đăng ký
POST   /api/users/login       - Đăng nhập
GET    /api/users/profile     - Thông tin profile
PUT    /api/users/profile     - Cập nhật profile
```

### 🛒 Cart Service (Port: 8003)
```
GET    /api/cart              - Xem giỏ hàng
POST   /api/cart/add          - Thêm sản phẩm
DELETE /api/cart/remove/{id}  - Xóa sản phẩm
PUT    /api/cart/update       - Cập nhật số lượng
```

## 🗂️ Cấu Trúc Dự Án

```
Software_Architecture_and_Design_PTIT/
├── user-service/
│   ├── src/main/java/
│   ├── src/main/resources/
│   └── pom.xml
├── product-service/
├── cart-service/
├── order-service/
├── search-service/
├── shipment-service/
├── payment-service/
├── review-service/
├── common/              # Shared utilities
├── docker-compose.yml   # Docker configuration
└── README.md
```

## 🛠️ Công Nghệ Sử Dụng

- **Backend Framework**: Spring Boot
- **Database**: MySQL/PostgreSQL
- **API Gateway**: Spring Cloud Gateway
- **Service Discovery**: Eureka
- **Message Queue**: RabbitMQ
- **Containerization**: Docker
- **Documentation**: Swagger/OpenAPI

## 🔄 Luồng Hoạt Động

1. **Đăng ký/Đăng nhập** → User Service
2. **Duyệt sản phẩm** → Product Service + Search Service
3. **Thêm vào giỏ** → Cart Service
4. **Đặt hàng** → Order Service
5. **Thanh toán** → Payment Service
6. **Vận chuyển** → Shipment Service
7. **Đánh giá** → Review Service

## 🧪 Testing

```bash
# Chạy unit tests
mvn test

# Chạy integration tests
mvn verify

# Test coverage
mvn jacoco:report
```

## 📚 Tài Liệu Tham Khảo

- [Spring Boot Documentation](https://spring.io/projects/spring-boot)
- [Microservices Pattern](https://microservices.io/)
- [Docker Documentation](https://docs.docker.com/)

## 👥 Nhóm Phát Triển

- **Môn học**: Kiến trúc và Thiết kế Phần mềm
- **Giảng viên**: Thầy TĐQ
- **Trường**: Học viện Công nghệ Bưu chính Viễn thông (PTIT)

---
⚡ **Lưu ý**: Đây là dự án học tập, không sử dụng cho mục đích thương mại.
