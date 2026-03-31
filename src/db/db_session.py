import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.models import Base


class DatabaseSession:

    SQLITE_PREFIX = "sqlite:///"
    DATABASE_URI = "chronicle.db"

    def __init__(self):
        directory_path = os.getenv("SQLITE_DATABASE_URL")
        database_url = f"{self.SQLITE_PREFIX}{directory_path}{self.DATABASE_URI}"
        self.engine = create_engine(database_url, connect_args={"check_same_thread": False})
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        # Create table on app startup if it doesn't exist
        Base.metadata.create_all(bind=self.engine)

    @contextmanager
    def get_session(self):
        """
        Creates a database session that is used as a context manager
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
