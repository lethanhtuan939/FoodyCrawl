# FoodyCrawl

FoodyCrawl là một ứng dụng web thu thập và hiển thị thông tin về các nhà hàng, quán ăn từ Foody.vn.

## Kiến trúc hệ thống

Dự án được xây dựng với kiến trúc microservices, bao gồm các thành phần chính:

- **Frontend**: Vue.js + Vite
- **Backend API**: FastAPI
- **Crawling Service**: FastAPI với các schedulers
- **Ingestion Service**: Python service để xử lý và lưu trữ dữ liệu
- **Database**: PostgreSQL
- **Nginx**: Reverse proxy server

## Cài đặt và Chạy

### Yêu cầu

- Docker
- Docker Compose

### Các bước cài đặt

1. Clone repository:
```bash
git clone <repository-url>
cd FoodyCrawl
```

2. Khởi động các services:
```bash
docker-compose up -d
```

3. Truy cập ứng dụng:
- Frontend: http://localhost
- Backend API docs: http://localhost/api/backend/docs
- Crawling API docs: http://localhost/api/crawling/docs

## Cấu trúc dự án

```
.
├── backend/                 # Backend API service
├── crawling/               # Crawling service
├── frontend/              # Vue.js frontend
├── ingestion/            # Data ingestion service
├── nginx/                # Nginx configuration
└── docker-compose.yml    # Docker compose configuration
```

### Backend Service
- FastAPI REST API
- PostgreSQL database
- API endpoints cho frontend

### Crawling Service
- Crawling data từ Foody.vn
- Lập lịch và quản lý crawling tasks
- API để kiểm soát crawling process

### Frontend
- Vue.js + Vite
- Giao diện người dùng
- Hiển thị dữ liệu từ backend

### Ingestion Service
- Xử lý dữ liệu từ crawling service
- Import dữ liệu vào database

## API Documentation

- Backend API: http://localhost/api/backend/docs
- Crawling API: http://localhost/api/crawling/docs

## Ports

- Frontend (Nginx): 80
- Backend: 8000
- Crawling Service: 8001
- PostgreSQL: 5432

## Contributing
