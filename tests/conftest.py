"""Test suite initialization."""

import pytest
from bot.config import config
from bot.database import db_manager


@pytest.fixture(scope="session")
def setup_test_db():
    """Setup test database."""
    db_manager.init_db()
    yield
    # Cleanup
    db_manager.close()


@pytest.fixture
def test_config():
    """Get test configuration."""
    return config
