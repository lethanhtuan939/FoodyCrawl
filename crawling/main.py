# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from controllers.crawling_controller import router as crawling_router
from controllers.scheduler_controller import start_scheduler, shutdown_scheduler

# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Tạo FastAPI app
app = FastAPI(title="FoodyCrawl API")

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký router
app.include_router(crawling_router)

# Khởi động scheduler khi app khởi chạy
@app.on_event("startup")
def on_startup():
    start_scheduler()

# Tắt scheduler khi app kết thúc
@app.on_event("shutdown")
def on_shutdown():
    shutdown_scheduler()
    