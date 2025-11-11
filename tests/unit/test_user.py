import pytest
from datetime import datetime
from models.user import User


class TestUserModel:
    """User类方法的白盒测试"""

    def test_user_initialization(self):
        """测试用户对象初始化"""
        user_id = "test_id"
        username = "test_user"
        password = "hashed_pwd"

        user = User(user_id, username, password)

        # 验证初始化属性
        assert user.user_id == user_id
        assert user.username == username
        assert user.password == password
        assert user.balance == 0.0
        assert user.is_frozen is False
        assert user.is_lost is False
        assert user.is_using is False
        assert user.session_token is None
        assert user.created_at is not None  # 初始化时应自动设置创建时间

    def test_to_dict_and_from_dict(self):
        """测试对象与字典的相互转换"""
        original_user = User(
            user_id="test_id",
            username="test_user",
            password="hashed_pwd",
            balance=1000.0,
            is_frozen=True,
            is_lost=False,
            is_using=True,
            session_token="test_token",
            last_login="2023-01-01T00:00:00"
        )
        original_user.created_at = "2023-01-01T00:00:00"

        # 转换为字典再重建对象
        user_dict = original_user.to_dict()
        restored_user = User.from_dict(user_dict)

        # 验证所有属性一致
        assert restored_user.user_id == original_user.user_id
        assert restored_user.balance == original_user.balance
        assert restored_user.is_frozen == original_user.is_frozen
        assert restored_user.session_token == original_user.session_token
        assert restored_user.created_at == original_user.created_at

    def test_generate_session_token(self):
        """测试会话令牌生成"""
        user = User("id", "user", "pwd")
        assert user.session_token is None

        # 生成令牌
        token = user.generate_session_token()

        # 验证令牌非空且状态更新
        assert token is not None
        assert user.session_token == token
        assert user.is_using is True
        assert user.last_login is not None  # 应更新登录时间

    def test_clear_session(self):
        """测试会话清除"""
        user = User("id", "user", "pwd")
        user.generate_session_token()  # 先创建会话
        assert user.session_token is not None
        assert user.is_using is True

        # 清除会话
        user.clear_session()

        assert user.session_token is None
        assert user.is_using is False

    def test_is_session_valid(self):
        """测试会话有效性验证（覆盖所有条件分支）"""
        user = User("id", "user", "pwd")
        valid_token = user.generate_session_token()

        # 分支1：令牌有效
        assert user.is_session_valid(valid_token) is True

        # 分支2：令牌无效（错误令牌）
        assert user.is_session_valid("invalid_token") is False

        # 分支3：用户未登录（is_using=False）
        user.is_using = False
        assert user.is_session_valid(valid_token) is False

        # 分支4：令牌为空
        user.session_token = None
        user.is_using = True
        assert user.is_session_valid(valid_token) is False

    def test_deposit(self):
        """测试存款功能（覆盖金额校验分支）"""
        user = User("id", "user", "pwd")

        # 分支1：正常存款（正数金额）
        assert user.deposit(500.0) is True
        assert user.balance == 500.0

        # 分支2：存款金额为0
        assert user.deposit(0.0) is False
        assert user.balance == 500.0  # 余额不变

        # 分支3：存款金额为负数
        assert user.deposit(-100.0) is False
        assert user.balance == 500.0  # 余额不变

    def test_withdraw(self):
        """测试取款功能（覆盖金额和余额校验分支）"""
        user = User("id", "user", "pwd")
        user.deposit(1000.0)  # 初始余额1000

        # 分支1：正常取款（金额合法且余额充足）
        assert user.withdraw(300.0) is True
        assert user.balance == 700.0

        # 分支2：取款金额为0
        assert user.withdraw(0.0) is False
        assert user.balance == 700.0

        # 分支3：取款金额为负数
        assert user.withdraw(-200.0) is False
        assert user.balance == 700.0

        # 分支4：余额不足
        assert user.withdraw(800.0) is False  # 当前余额700
        assert user.balance == 700.0

    def test_account_status_operations(self):
        """测试账户状态操作（挂失、冻结、解冻）"""
        user = User("id", "user", "pwd")

        # 测试挂失
        user.report_loss()
        assert user.is_lost is True

        # 测试冻结
        user.freeze_account()
        assert user.is_frozen is True

        # 测试解冻
        user.unfreeze_account()
        assert user.is_frozen is False