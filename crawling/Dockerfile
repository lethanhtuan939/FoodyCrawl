FROM python:3.9-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Thiết lập biến môi trường
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Ho_Chi_Minh

# Cài đặt các dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Tạo thư mục lưu data và logs
RUN mkdir -p /app/landing_zone && chmod -R 777 /app/landing_zone
RUN mkdir -p /app/logs && chmod -R 777 /app/logs

# Copy code vào container
COPY . .

# Expose port 8000 để kết nối từ bên ngoài
EXPOSE 8000

# Khởi chạy ứng dụng khi container chạy
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
