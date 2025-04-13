from sqlalchemy import Column, Integer, String,Boolean, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from sqlalchemy.sql import func


Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    client_key = Column(String, unique=True, index=True)
    secret_key = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    
# DB Config
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db():
    Base.metadata.create_all(bind=engine)
