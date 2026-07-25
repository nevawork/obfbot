"""Permission system for the bot."""

from typing import Optional
from enum import Enum
from bot.config import config
from bot.logger import logger


class Permission(str, Enum):
    """Permission levels."""

    USER = "user"
    PREMIUM = "premium"
    ADMIN = "admin"
    OWNER = "owner"


class PermissionManager:
    """Manage user permissions."""

    def __init__(self):
        """Initialize permission manager."""
        self.cache = {}

    def get_user_permission(self, user_id: int) -> Permission:
        """Get user permission level.

        Args:
            user_id: User ID

        Returns:
            Permission level
        """
        if user_id == config.BOT_OWNER_ID:
            return Permission.OWNER

        if config.BOT_ADMIN_ROLE_ID and hasattr(self, "_check_role"):
            if self._check_role(user_id, config.BOT_ADMIN_ROLE_ID):
                return Permission.ADMIN

        if config.BOT_PREMIUM_ROLE_ID and hasattr(self, "_check_role"):
            if self._check_role(user_id, config.BOT_PREMIUM_ROLE_ID):
                return Permission.PREMIUM

        return Permission.USER

    def has_permission(self, user_id: int, required: Permission) -> bool:
        """Check if user has required permission.

        Args:
            user_id: User ID
            required: Required permission level

        Returns:
            True if user has permission
        """
        user_perm = self.get_user_permission(user_id)
        perm_levels = {
            Permission.USER: 1,
            Permission.PREMIUM: 2,
            Permission.ADMIN: 3,
            Permission.OWNER: 4,
        }
        return perm_levels.get(user_perm, 0) >= perm_levels.get(required, 0)

    def is_owner(self, user_id: int) -> bool:
        """Check if user is bot owner.

        Args:
            user_id: User ID

        Returns:
            True if owner
        """
        return user_id == config.BOT_OWNER_ID

    def is_admin(self, user_id: int) -> bool:
        """Check if user is admin.

        Args:
            user_id: User ID

        Returns:
            True if admin
        """
        return self.has_permission(user_id, Permission.ADMIN)

    def is_premium(self, user_id: int) -> bool:
        """Check if user is premium.

        Args:
            user_id: User ID

        Returns:
            True if premium
        """
        return self.has_permission(user_id, Permission.PREMIUM)

    def cache_clear(self) -> None:
        """Clear permission cache."""
        self.cache.clear()
        logger.info("Permission cache cleared")


permission_manager = PermissionManager()
