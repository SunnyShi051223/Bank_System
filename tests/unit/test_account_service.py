import pytest
from unittest.mock import patch, MagicMock
from services.account_service import AccountService
from models.user import User  # 确保导入User类


class TestAccountService:
    """AccountService类的白盒测试"""

    # 新增test_user夹具定义（或确保conftest.py中的夹具可被继承）
    @pytest.fixture
    def test_user(self):
        """提供测试用的User实例"""
        return User(
            user_id="test_user_id",
            username="testuser",
            password="hashed_password",
            is_using=False,
            is_lost=False,
            is_frozen=False
        )

    @pytest.fixture
    def account_service(self):
        """提供带有模拟DataManager的AccountService实例"""
        with patch('services.account_service.DataManager') as mock_dm:
            service = AccountService()
            service.data_manager = mock_dm.return_value
            yield service

    def test_report_loss_success(self, account_service, test_user):
        """测试账户挂失成功流程"""
        # 配置模拟：更新用户成功
        account_service.data_manager.update_user.return_value = True

        # 执行挂失
        success, message = account_service.report_loss(test_user)

        # 验证结果
        assert success is True
        assert "挂失成功" in message
        assert test_user.is_lost is True  # 状态应更新
        account_service.data_manager.update_user.assert_called_once_with(test_user)

    def test_report_loss_already_lost(self, account_service, test_user):
        """测试已挂失账户再次挂失（分支覆盖）"""
        test_user.is_lost = True  # 预先设置为已挂失

        success, message = account_service.report_loss(test_user)

        assert success is False
        assert "已挂失" in message
        account_service.data_manager.update_user.assert_not_called()  # 不应调用更新

    def test_freeze_account_success(self, account_service, test_user):
        """测试账户冻结成功流程"""
        account_service.data_manager.update_user.return_value = True

        success, message = account_service.freeze_account(test_user)

        assert success is True
        assert "冻结成功" in message
        assert test_user.is_frozen is True
        account_service.data_manager.update_user.assert_called_once()

    def test_freeze_account_already_frozen(self, account_service, test_user):
        """测试已冻结账户再次冻结（分支覆盖）"""
        test_user.is_frozen = True

        success, message = account_service.freeze_account(test_user)

        assert success is False
        assert "已冻结" in message
        account_service.data_manager.update_user.assert_not_called()

    def test_unfreeze_account_success(self, account_service, test_user):
        """测试账户解冻成功流程"""
        test_user.is_frozen = True  # 预先冻结
        account_service.data_manager.update_user.return_value = True

        success, message = account_service.unfreeze_account(test_user)

        assert success is True
        assert "解冻成功" in message
        assert test_user.is_frozen is False
        account_service.data_manager.update_user.assert_called_once()

    def test_unfreeze_account_not_frozen(self, account_service, test_user):
        """测试未冻结账户解冻（分支覆盖）"""
        success, message = account_service.unfreeze_account(test_user)

        assert success is False
        assert "未冻结" in message
        account_service.data_manager.update_user.assert_not_called()

    def test_close_account_success(self, account_service, test_user):
        """测试账户销户成功流程"""
        account_service.data_manager.delete_user.return_value = True

        success, message = account_service.close_account(test_user)

        assert success is True
        assert "账户注销成功" in message
        account_service.data_manager.delete_user.assert_called_once_with(test_user.user_id)

    def test_close_account_failure(self, account_service, test_user):
        """测试账户销户失败（数据删除失败）"""
        account_service.data_manager.delete_user.return_value = False  # 模拟删除失败

        success, message = account_service.close_account(test_user)

        assert success is False
        assert "销户失败" in message