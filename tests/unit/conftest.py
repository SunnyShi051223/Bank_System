import pytest
from unittest.mock import patch, MagicMock
from models.user import User
from services.user_service import UserService

@pytest.fixture
def mock_data_manager():
    with patch('services.user_service.DataManager') as mock_dm:
        yield mock_dm

@pytest.fixture
def user_service(mock_data_manager):
    service = UserService()
    service.data_manager = mock_data_manager.return_value
    return service

@pytest.fixture
def test_user():
    return User(
        user_id="test_user_id",
        username="testuser",
        password="hashed_password",
        is_using=False,
        is_lost=False,
        is_frozen=False
    )
