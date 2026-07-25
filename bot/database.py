"""Database models and management."""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from bot.config import config
from bot.logger import logger

Base = declarative_base()


class User(Base):
    """User model for tracking bot users."""

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    is_premium = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    is_blacklisted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_used = Column(DateTime, nullable=True)


class Job(Base):
    """Job model for tracking obfuscation tasks."""

    __tablename__ = "jobs"

    job_id = Column(String(36), primary_key=True)  # UUID
    user_id = Column(Integer, nullable=False)
    filename = Column(String(255), nullable=False)
    status = Column(String(50), default="queued")  # queued, processing, completed, failed, cancelled
    input_size = Column(Integer, nullable=False)  # bytes
    output_size = Column(Integer, nullable=True)  # bytes
    processing_time = Column(Float, nullable=True)  # seconds
    obfuscation_level = Column(Integer, default=5)
    error_message = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    settings = Column(JSON, default={})


class JobStatistics(Base):
    """Statistics for each job."""

    __tablename__ = "job_statistics"

    stat_id = Column(String(36), primary_key=True)
    job_id = Column(String(36), nullable=False)
    identifiers_renamed = Column(Integer, default=0)
    strings_encrypted = Column(Integer, default=0)
    numbers_encoded = Column(Integer, default=0)
    functions_wrapped = Column(Integer, default=0)
    dead_code_inserted = Column(Integer, default=0)
    control_flow_flattened = Column(Boolean, default=False)
    protection_summary = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserStatistics(Base):
    """User statistics model."""

    __tablename__ = "user_statistics"

    stat_id = Column(String(36), primary_key=True)
    user_id = Column(Integer, primary_key=True)
    total_jobs = Column(Integer, default=0)
    successful_jobs = Column(Integer, default=0)
    failed_jobs = Column(Integer, default=0)
    total_input_bytes = Column(Integer, default=0)
    total_output_bytes = Column(Integer, default=0)
    total_processing_time = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserSettings(Base):
    """User settings model."""

    __tablename__ = "user_settings"

    setting_id = Column(String(36), primary_key=True)
    user_id = Column(Integer, primary_key=True)
    obfuscation_level = Column(Integer, default=5)
    rename_variables = Column(Boolean, default=True)
    encrypt_strings = Column(Boolean, default=True)
    encrypt_constants = Column(Boolean, default=True)
    flatten_control_flow = Column(Boolean, default=True)
    dead_code_amount = Column(Integer, default=5)
    runtime_size = Column(String(50), default="medium")  # small, medium, large
    anti_tamper = Column(Boolean, default=True)
    anti_debug = Column(Boolean, default=False)
    compression = Column(Boolean, default=False)
    output_formatting = Column(String(50), default="minified")  # minified, formatted
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RateLimit(Base):
    """Rate limiting model."""

    __tablename__ = "rate_limits"

    limit_id = Column(String(36), primary_key=True)
    user_id = Column(Integer, primary_key=True)
    requests = Column(Integer, default=0)
    window_start = Column(DateTime, default=datetime.utcnow)
    window_end = Column(DateTime, nullable=False)


class DatabaseManager:
    """Database connection and session management."""

    def __init__(self):
        """Initialize database manager."""
        self.engine = create_engine(
            config.DATABASE_URL,
            echo=config.SQLALCHEMY_ECHO,
            connect_args={"check_same_thread": False} if "sqlite" in config.DATABASE_URL else {},
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def init_db(self) -> None:
        """Initialize database tables."""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    def get_session(self) -> Session:
        """Get a database session."""
        return self.SessionLocal()

    def close(self) -> None:
        """Close database connection."""
        self.engine.dispose()
        logger.info("Database connection closed")


# Global database manager
db_manager = DatabaseManager()
