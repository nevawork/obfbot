"""Rate limiting functionality."""

from typing import Optional
from datetime import datetime, timedelta
from bot.config import config
from bot.logger import logger


class RateLimiter:
    """Rate limiting for users."""

    def __init__(self):
        """Initialize rate limiter."""
        self.limits: dict = {}  # user_id -> (requests, window_start)

    def is_rate_limited(self, user_id: int, is_premium: bool = False) -> bool:
        """Check if user is rate limited.

        Args:
            user_id: User ID
            is_premium: Whether user is premium

        Returns:
            True if rate limited
        """
        now = datetime.utcnow()
        max_requests = (
            config.PREMIUM_RATE_LIMIT_REQUESTS if is_premium else config.RATE_LIMIT_REQUESTS
        )
        window = config.RATE_LIMIT_WINDOW_SECONDS

        if user_id not in self.limits:
            self.limits[user_id] = (1, now)
            return False

        requests, window_start = self.limits[user_id]
        elapsed = (now - window_start).total_seconds()

        if elapsed > window:
            # New window
            self.limits[user_id] = (1, now)
            return False

        if requests >= max_requests:
            remaining = window - elapsed
            logger.warning(
                f"User {user_id} rate limited. Reset in {remaining:.0f}s"
            )
            return True

        self.limits[user_id] = (requests + 1, window_start)
        return False

    def get_remaining(self, user_id: int, is_premium: bool = False) -> int:
        """Get remaining requests for user.

        Args:
            user_id: User ID
            is_premium: Whether user is premium

        Returns:
            Remaining requests
        """
        max_requests = (
            config.PREMIUM_RATE_LIMIT_REQUESTS if is_premium else config.RATE_LIMIT_REQUESTS
        )

        if user_id not in self.limits:
            return max_requests

        requests, _ = self.limits[user_id]
        return max(0, max_requests - requests)

    def reset_user(self, user_id: int) -> None:
        """Reset user rate limit.

        Args:
            user_id: User ID
        """
        if user_id in self.limits:
            del self.limits[user_id]
            logger.info(f"Rate limit reset for user {user_id}")


rate_limiter = RateLimiter()
