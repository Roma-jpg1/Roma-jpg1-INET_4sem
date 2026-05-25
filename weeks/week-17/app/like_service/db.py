from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import time
time.sleep(10)

DATABASE_URL = "postgresql://postgres:postgres@like-db:5432/like_service_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, 
                            autoflush=False, 
                            bind=engine)

Base = declarative_base()