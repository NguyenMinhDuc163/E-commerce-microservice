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

## 🚀 Hướng Dẫn Cài Đặt

### Yêu Cầu Hệ Thống
- **Java**: 11 hoặc cao hơn
- **Maven**: 3.6+
- **Database**: MySQL/PostgreSQL
- **IDE**: IntelliJ IDEA hoặc Eclipse

### Cài Đặt và Chạy

1. **Clone repository**
   ```bash
   git clone [repository-url]
   cd Software_Architecture_and_Design_PTIT
   ```

2. **Cài đặt dependencies**
   ```bash
   mvn clean install
   ```

3. **Cấu hình database**
   - Tạo database cho mỗi service
   - Cập nhật file `application.properties` trong mỗi service

4. **Chạy các services** (theo thứ tự)
   ```bash
   # Chạy từng service trên port tương ứng
   mvn spring-boot:run -Dspring-boot.run.profiles=dev
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