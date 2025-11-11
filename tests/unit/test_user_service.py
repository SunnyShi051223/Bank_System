import pytest
from unittest.mock import patch, MagicMock
from models.user import User

class TestUserService:
    """Test cases for UserService class."""

    def test_register_success(self, user_service, mock_data_manager, test_user):
        """Test successful user registration."""
        # Setup
        username = "newuser"
        password = "secure123"
        
        # Configure the mock to return None (user doesn't exist)
        mock_data_manager.return_value.find_user_by_username.return_value = None
        mock_data_manager.return_value.add_user.return_value = True
        
        # Execute
        success, message = user_service.register(username, password)
        
        # Verify
        assert success is True
        assert "成功" in message
        mock_data_manager.return_value.add_user.assert_called_once()

    def test_register_existing_username(self, user_service, mock_data_manager, test_user):
        """Test registration with an existing username."""
        # Setup
        username = "existinguser"
        password = "password123"
        
        # Configure the mock to return a user (username exists)
        mock_data_manager.return_value.find_user_by_username.return_value = test_user
        
        # Execute
        success, message = user_service.register(username, password)
        
        # Verify
        assert success is False
        assert "已存在" in message
        mock_data_manager.return_value.add_user.assert_not_called()

    def test_login_success(self, user_service, mock_data_manager, test_user):
        """Test successful user login."""
        # Setup
        username = "testuser"
        password = "correctpassword"
        
        # Configure test user with known password hash
        # The hash of "correctpassword" using SHA-256
        test_user.password = "21e721c35a5823fdb452fa2f9f0a612c74fb952e06927489c6b27a43b817bed4"
        
        # Configure mocks
        mock_data_manager.return_value.find_user_by_username.return_value = test_user
        mock_data_manager.return_value.update_user.return_value = True
        
        # Execute
        success, message, user, session_token = user_service.login(username, password)
        
        # Verify
        assert success is True
        assert "成功" in message
        assert user is not None
        assert session_token is not None
        assert user.is_using is True
        assert user.session_token is not None

    def test_login_wrong_password(self, user_service, mock_data_manager, test_user):
        """Test login with wrong password."""
        # Setup
        username = "testuser"
        wrong_password = "wrongpassword"
        
        # Configure test user with known password hash
        test_user.password = "21e721c35a5823fdb452fa2f9f0a612c74fb952e06927489c6b27a43b817bed4"  # hash of "correctpassword"
        
        # Configure mocks
        mock_data_manager.return_value.find_user_by_username.return_value = test_user
        
        # Execute
        success, message, user, session_token = user_service.login(username, wrong_password)
        
        # Verify
        assert success is False
        assert "密码错误" in message
        assert user is None
        assert session_token is None

    def test_logout_success(self, user_service, mock_data_manager, test_user):
        """Test successful user logout."""
        # Setup
        test_user.is_using = True
        test_user.session_token = "test_session_token"
        
        # Configure mocks
        mock_data_manager.return_value.update_user.return_value = True
        
        # Execute
        success, message = user_service.logout(test_user)
        
        # Verify
        assert success is True
        assert "成功" in message
        assert test_user.is_using is False
        assert test_user.session_token is None
        mock_data_manager.return_value.update_user.assert_called_once_with(test_user)

    def test_validate_session_valid(self, user_service, mock_data_manager, test_user):
        """Test validating a valid session."""
        # Setup
        test_user.is_using = True
        test_user.session_token = "valid_token"
        
        # Configure mocks
        mock_data_manager.return_value.find_user_by_id.return_value = test_user
        
        # Execute
        is_valid, user = user_service.validate_session("test_user_id", "valid_token")
        
        # Verify
        assert is_valid is True
        assert user is not None
        assert user.user_id == "test_user_id"

    def test_validate_session_invalid(self, user_service, mock_data_manager, test_user):
        """Test validating an invalid session."""
        # Setup
        test_user.is_using = True
        test_user.session_token = "valid_token"
        
        # Configure mocks
        mock_data_manager.return_value.find_user_by_id.return_value = test_user
        
        # Execute with wrong token
        is_valid, user = user_service.validate_session("test_user_id", "invalid_token")
        
        # Verify
        assert is_valid is False
        assert user is None
