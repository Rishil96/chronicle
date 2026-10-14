from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import settings
from src.db.models import Base


# Create Database Engine
connect_args = {"check_same_thread": False} if settings.db_driver == "sqlite" else {}
engine = create_engine(settings.database_url, connect_args=connect_args)

# Create Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create table on app startup if it doesn't exist
Base.metadata.create_all(bind=engine)

# Function to inject Database dependency
def get_db():
    with SessionLocal() as db:
        yield db
