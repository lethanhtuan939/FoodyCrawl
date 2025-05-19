from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from controllers.crawling_controller import router as crawling_router
from controllers.scheduler_controller import start_scheduler, shutdown_scheduler
from utils.logging_utils import setup_logging

# Thiết lập logging
logger = setup_logging(logging.INFO)

# Tạo FastAPI app
app = FastAPI(
    title="FoodyCrawl API",
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url="/redoc",
    root_path="/api/crawling")

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
    logger.info("Starting FoodyCrawl application...")
    start_scheduler()
    logger.info("Scheduler has been started")

# Tắt scheduler khi app kết thúc
@app.on_event("shutdown")
def on_shutdown():
    logger.info("Shutting down FoodyCrawl application...")
    shutdown_scheduler()
    logger.info("Scheduler has been stopped")