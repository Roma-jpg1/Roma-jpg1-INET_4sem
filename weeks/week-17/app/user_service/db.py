import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

time.sleep(10)
    

DATABASE_URL = "postgresql://postgres:postgres@user-db:5432/user_service_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, 
                            autoflush=False, 
                            bind=engine)

Base = declarative_base()