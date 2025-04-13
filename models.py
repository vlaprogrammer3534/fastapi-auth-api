# -------------------------------------------
# models.py - SQLAlchemy ORM Model Definition
# -------------------------------------------

from sqlalchemy import Column, Integer, String, Boolean, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Base class for all database models
Base = declarative_base()

# -------------------------------
# User Model - Represents a user
# -------------------------------
class User(Base):
    __tablename__ = "users"  # Name of the table in the database

    id = Column(Integer, primary_key=True, index=True)  # Primary key
    client_key = Column(String, unique=True, index=True)  # Unique client key (like username or app key)
    secret_key = Column(String)  # Secret key for authentication (like a password or token)
    created_at = Column(DateTime, default=datetime.utcnow)  # Timestamp of user creation

# -----------------------------------------
# Database Configuration and Setup Section
# -----------------------------------------

# SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create a database engine with SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite in multi-threaded apps
)

# Create a session factory for DB operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to create tables (run once during setup)
def create_db():
    Base.metadata.create_all(bind=engine)
