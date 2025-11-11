import pytest
from unittest.mock import MagicMock, patch
from models.user import User

class TestTransactionService:
    """Test cases for TransactionService class."""

    @pytest.fixture
    def transaction_service(self):
        """Fixture that provides a TransactionService instance with a mocked DataManager."""
        with patch('services.transaction_service.DataManager') as mock:
            from services.transaction_service import TransactionService
            return TransactionService()

    @pytest.fixture
    def active_user(self):
        """Fixture that provides an active test user with balance."""
        user = User(
            user_id="test_user_id",
            username="testuser",
            password="hashed_password",
            is_using=True,
            is_lost=False,
            is_frozen=False
        )
        user.balance = 1000.0  # Set initial balance
        return user

    def test_deposit_success(self, transaction_service, active_user):
        """Test successful deposit."""
        # Setup
        amount = 500.0
        initial_balance = active_user.balance
        
        # Configure mocks
        transaction_service.data_manager.update_user.return_value = True
        
        # Execute
        success, message, new_balance = transaction_service.deposit(active_user, amount)
        
        # Verify
        assert success is True
        assert "成功" in message
        assert new_balance == initial_balance + amount
        transaction_service.data_manager.update_user.assert_called_once_with(active_user)

    def test_deposit_invalid_amount(self, transaction_service, active_user):
        """Test deposit with invalid (negative) amount."""
        # Setup
        initial_balance = active_user.balance
        
        # Execute with negative amount
        success, message, new_balance = transaction_service.deposit(active_user, -100.0)
        
        # Verify
        assert success is False
        assert "必须大于0" in message
        assert new_balance == initial_balance
        transaction_service.data_manager.update_user.assert_not_called()

    def test_withdraw_success(self, transaction_service, active_user):
        """Test successful withdrawal."""
        # Setup
        amount = 200.0
        initial_balance = active_user.balance
        
        # Configure mocks
        transaction_service.data_manager.update_user.return_value = True
        
        # Execute
        success, message, new_balance = transaction_service.withdraw(active_user, amount)
        
        # Verify
        assert success is True
        assert "成功" in message
        assert new_balance == initial_balance - amount
        transaction_service.data_manager.update_user.assert_called_once_with(active_user)

    def test_withdraw_insufficient_balance(self, transaction_service, active_user):
        """Test withdrawal with insufficient balance."""
        # Setup
        amount = active_user.balance + 100.0  # More than balance
        initial_balance = active_user.balance
        
        # Execute
        success, message, new_balance = transaction_service.withdraw(active_user, amount)
        
        # Verify
        assert success is False
        assert "余额不足" in message
        assert new_balance == initial_balance
        transaction_service.data_manager.update_user.assert_not_called()

    def test_withdraw_invalid_amount(self, transaction_service, active_user):
        """Test withdrawal with invalid (negative) amount."""
        # Setup
        initial_balance = active_user.balance
        
        # Execute with negative amount
        success, message, new_balance = transaction_service.withdraw(active_user, -100.0)
        
        # Verify
        assert success is False
        assert "必须大于0" in message
        assert new_balance == initial_balance
        transaction_service.data_manager.update_user.assert_not_called()

    def test_check_balance(self, transaction_service, active_user):
        """Test checking account balance."""
        # Setup
        expected_balance = active_user.balance
        
        # Execute
        success, message, balance = transaction_service.check_balance(active_user)
        
        # Verify
        assert success is True
        assert "成功" in message
        assert balance == expected_balance

    def test_deposit_lost_account(self, transaction_service, active_user):
        """Test deposit to a lost account."""
        # Setup
        active_user.is_lost = True
        initial_balance = active_user.balance
        
        # Execute
        success, message, balance = transaction_service.deposit(active_user, 100.0)
        
        # Verify
        assert success is False
        assert "挂失" in message
        assert balance == initial_balance
        transaction_service.data_manager.update_user.assert_not_called()

    def test_withdraw_frozen_account(self, transaction_service, active_user):
        """Test withdrawal from a frozen account."""
        # Setup
        active_user.is_frozen = True
        initial_balance = active_user.balance
        
        # Execute
        success, message, balance = transaction_service.withdraw(active_user, 100.0)
        
        # Verify
        assert success is False
        assert "冻结" in message
        assert balance == initial_balance
        transaction_service.data_manager.update_user.assert_not_called()
