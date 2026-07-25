"""Configuration management for the obfuscation bot."""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Main configuration class."""

    # Discord
    DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN", "")
    DISCORD_PREFIX: str = os.getenv("DISCORD_PREFIX", "/")
    BOT_OWNER_ID: int = int(os.getenv("BOT_OWNER_ID", "0"))
    BOT_ADMIN_ROLE_ID: Optional[int] = (
        int(os.getenv("BOT_ADMIN_ROLE_ID")) if os.getenv("BOT_ADMIN_ROLE_ID") else None
    )
    BOT_PREMIUM_ROLE_ID: Optional[int] = (
        int(os.getenv("BOT_PREMIUM_ROLE_ID")) if os.getenv("BOT_PREMIUM_ROLE_ID") else None
    )

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./obfbot.db")
    SQLALCHEMY_ECHO: bool = os.getenv("SQLALCHEMY_ECHO", "false").lower() == "true"

    # Processing
    MAX_QUEUE_SIZE: int = int(os.getenv("MAX_QUEUE_SIZE", "500"))
    MAX_CONCURRENT_JOBS: int = int(os.getenv("MAX_CONCURRENT_JOBS", "10"))
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "25"))
    MAX_FILE_SIZE_BYTES: int = MAX_FILE_SIZE_MB * 1024 * 1024
    JOB_TIMEOUT_SECONDS: int = int(os.getenv("JOB_TIMEOUT_SECONDS", "300"))
    CLEANUP_INTERVAL_SECONDS: int = int(os.getenv("CLEANUP_INTERVAL_SECONDS", "3600"))

    # Obfuscation Defaults
    DEFAULT_OBFUSCATION_LEVEL: int = int(os.getenv("DEFAULT_OBFUSCATION_LEVEL", "5"))
    MAX_OBFUSCATION_LEVEL: int = int(os.getenv("MAX_OBFUSCATION_LEVEL", "10"))

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "10"))
    RATE_LIMIT_WINDOW_SECONDS: int = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "3600"))
    PREMIUM_RATE_LIMIT_REQUESTS: int = int(os.getenv("PREMIUM_RATE_LIMIT_REQUESTS", "50"))

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/obfbot.log")

    # API
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_ENABLED: bool = os.getenv("API_ENABLED", "false").lower() == "true"

    # Storage
    TEMP_DIR: Path = Path(os.getenv("TEMP_DIR", "./temp"))
    OUTPUT_DIR: Path = Path(os.getenv("OUTPUT_DIR", "./output"))
    BACKUP_DIR: Path = Path(os.getenv("BACKUP_DIR", "./backups"))

    @classmethod
    def init_directories(cls) -> None:
        """Initialize required directories."""
        cls.TEMP_DIR.mkdir(parents=True, exist_ok=True)
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        cls.BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        Path("logs").mkdir(parents=True, exist_ok=True)

    @classmethod
    def validate(cls) -> bool:
        """Validate configuration."""
        if not cls.DISCORD_TOKEN:
            raise ValueError("DISCORD_TOKEN is not set")
        if cls.BOT_OWNER_ID == 0:
            raise ValueError("BOT_OWNER_ID is not set")
        return True


config = Config()
