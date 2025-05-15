from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from time import sleep

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "123456")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "foody")

DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"

for _ in range(5):
    try:
        engine = create_engine(DATABASE_URL)
        engine.connect()
        print("Connected to PostgreSQL successfully.")
        break
    except Exception as e:
        print(f"Connection failed: {e}")
        sleep(5)
else:
    raise Exception("Cannot connect to PostgreSQL after multiple attempts")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Định nghĩa bảng locations
class LocationDB(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, unique=True, index=True)
    country_id = Column(Integer)
    name = Column(String)
    country_name = Column(String)

# Định nghĩa bảng foods
class FoodDB(Base):
    __tablename__ = "foods"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    categories = Column(ARRAY(String))
    cuisines = Column(ARRAY(String))
    address = Column(String)
    rating_avg = Column(Float)
    rating_total_review = Column(Integer)
    is_open = Column(Boolean)
    city_id = Column(Integer, ForeignKey("locations.city_id"), nullable=True)
    
def init_db():
    Base.metadata.create_all(bind=engine)