from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import settings
from src.db.models import Base


class DatabaseSession:

    def __init__(self):
        database_url = settings.database_url
        connect_args = {"check_same_thread": False} if settings.db_driver == "sqlite" else {}
        self.engine = create_engine(database_url, connect_args=connect_args)
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
