"""ObfBot - Advanced Lua/Luau Obfuscator Discord Bot."""

__version__ = "1.0.0"
__author__ = "nevawork"

from bot.config import config
from bot.database import db_manager
from bot.queue import JobQueue
from bot.permissions import permission_manager
from bot.logger import logger

__all__ = [
    "config",
    "db_manager",
    "JobQueue",
    "permission_manager",
    "logger",
]
