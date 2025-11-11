import pytest
from unittest.mock import MagicMock, patch
from models.user import User

@pytest.fixture
def mock_data_manager():
    """Fixture to mock the DataManager class."""
    with patch('services.user_service.DataManager') as mock:
        yield mock

@pytest.fixture
def user_service(mock_data_manager):
    """Fixture that provides a UserService instance with a mocked DataManager."""
    from services.user_service import UserService
    return UserService()

@pytest.fixture
def test_user():
    """Fixture that provides a test user."""
    return User(
        user_id="test_user_id",
        username="testuser",
        password="hashed_password",
        is_using=False,
        is_lost=False,
        is_frozen=False
    )
