# Foody Crawling Service

Service để crawl dữ liệu từ Foody.vn, bao gồm thông tin về các địa điểm và nhà hàng.

## Cấu trúc dữ liệu

Dữ liệu được lưu trong file JSON với cấu trúc:
```json
{
    "locations": [
        {
            "city_id": 218,
            "country_id": 1,
            "name": "Hồ Chí Minh",
            "country_name": "Việt Nam"
        },
        ...
    ],
    "foods": [
        {
            "name": "Tên nhà hàng",
            "categories": "Danh mục 1, Danh mục 2",
            "cuisines": "Món 1, Món 2",
            "address": "Địa chỉ nhà hàng",
            "rating_avg": 4.5,
            "rating_total_review": 100,
            "is_open": true,
            "city_id": 218
        },
        ...
    ]
}
```

## API Endpoints

### 1. Crawl Locations
```http
GET /api/crawl-locations
```
Crawl danh sách các địa điểm từ Foody.vn.

### 2. Crawl Browsing IDs
```http
GET /api/crawl-browsing-ids?city_id=218
```
Crawl danh sách delivery IDs cho một thành phố cụ thể.

### 3. Crawl By City
```http
GET /api/crawl-by-city?city_id=218
```
Crawl toàn bộ thông tin nhà hàng cho một thành phố cụ thể.

### 4. Full Crawl
```http
GET /api/full-crawl
```
Thực hiện crawl toàn bộ:
1. Crawl danh sách địa điểm
2. Với mỗi địa điểm, crawl danh sách delivery IDs
3. Với mỗi delivery ID, crawl thông tin chi tiết nhà hàng
4. Lưu tất cả dữ liệu vào một file JSON duy nhất (Hiện tại chỉ cần dùng API này)

## Scheduler

Service có tích hợp scheduler để tự động crawl dữ liệu theo lịch:

### Cấu hình Scheduler
- Sử dụng APScheduler để quản lý các tác vụ theo lịch
- Mặc định chạy full crawl mỗi ngày vào lúc 14:02
- Có thể cấu hình thời gian chạy bằng cách sửa đổi CronTrigger trong `scheduler_controller.py`

### Cách hoạt động
1. Scheduler tự động khởi động khi service được chạy
2. Mỗi ngày vào thời điểm đã cấu hình, scheduler sẽ:
   - Thực hiện full crawl
   - Lưu dữ liệu vào file JSON mới
   - Ghi log kết quả crawl
3. Scheduler tự động tắt khi service dừng

### Cấu hình thời gian
Để thay đổi thời gian chạy scheduler, sửa đổi CronTrigger trong `scheduler_controller.py`:
```python
scheduler.add_job(
    scheduled_full_crawl,
    CronTrigger(hour=14, minute=2),  # Thay đổi giờ và phút ở đây
    id="daily_full_crawl",
    name="Daily full crawl",
    replace_existing=True
)
```

## Cấu hình

- `MAX_DELIVERY_IDS_PER_CITY`: Số lượng delivery IDs tối đa sẽ crawl cho mỗi thành phố (mặc định: 1)
- `LANDING_ZONE_PATH`: Thư mục lưu trữ file JSON kết quả
  - Trong Docker: `/app/landing_zone`
  - Trong môi trường development: `[project_root]/landing_zone`

## Cài đặt và Chạy

### Yêu cầu
- Python 3.8+
- FastAPI
- Uvicorn
- APScheduler

### Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Chạy service
```bash
uvicorn main:app --reload
```

## Lưu ý

1. Service có cơ chế delay ngẫu nhiên giữa các request để tránh bị block
2. Mỗi request sẽ delay từ 0.5 đến 1.0 giây
3. File JSON kết quả sẽ được lưu trong thư mục `landing_zone` với tên file dạng `foody_combined_data_[timestamp].json`
4. Scheduler sẽ tự động chạy full crawl mỗi ngày và lưu kết quả vào file mới

## Error Handling

Service sẽ trả về lỗi với format:
```json
{
    "status": "error",
    "message": "Mô tả lỗi",
    "data": null
}
```

Các lỗi phổ biến:
- 500: Lỗi server
- 404: Không tìm thấy resource
- 400: Request không hợp lệ