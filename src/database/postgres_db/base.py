import time
import logging
from threading import Lock

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from database.config import BaseConfig as Conf


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


class PostgresConnector(object):
    _instance = None  # Singleton instance
    _lock = Lock()  # Thread safety for singleton initialization

    def __new__(cls):
        """ Implementing Singleton Pattern with Thread-Safety """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-check locking
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """ Initialize the database engine and session factory with retry logic """
        max_retries = 3
        retry_delay = 2  # Seconds between retries

        for attempt in range(1, max_retries + 1):
            try:
                self.engine = create_engine(
                    Conf.POSTGRES_CONNECTION_URL,
                    pool_size=10,
                    max_overflow=20,
                )
                self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
                Base.metadata.create_all(self.engine)

                # Test the connection
                with self.engine.connect() as connection:
                    connection.execute(text("SELECT 1"))

                logger.info("PostgreSQL connection established successfully.")
                return
            except Exception as e:
                logger.error(f"Error connecting to PostgreSQL (Attempt {attempt}/{max_retries}): {e}")
                if attempt < max_retries:
                    time.sleep(retry_delay)
                else:
                    raise Exception("Failed to connect to PostgreSQL after multiple retries.")

    def get_db(self):
        """ FastAPI Dependency Injection: Provides a new session """
        session = self.SessionLocal()
        try:
            yield session
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()

    def __enter__(self):
        """ Enable use as a context manager (with PostgresConnector() as db:) """
        self.session = self.SessionLocal()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Ensure the session is closed after usage """
        if exc_type:
            self.session.rollback()
            logger.error(f"Exception in DB session: {exc_val}")
        self.session.close()
