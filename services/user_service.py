import hashlib
import uuid
from typing import Optional
from models.user import User
from utils.data_manager import DataManager


class UserService:
    def __init__(self):
        self.data_manager = DataManager()

    def _hash_password(self, password: str) -> str:
        """对密码进行哈希处理"""
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username: str, password: str) -> tuple[bool, str]:
        """用户注册"""
        # 检查用户名是否已存在
        if self.data_manager.find_user_by_username(username):
            return False, "用户名已存在"

        # 创建新用户
        user_id = str(uuid.uuid4())
        hashed_password = self._hash_password(password)
        new_user = User(user_id, username, hashed_password)

        # 保存用户
        if self.data_manager.add_user(new_user):
            return True, "注册成功"
        else:
            return False, "注册失败，请稍后重试"

    def login(self, username: str, password: str) -> tuple[bool, str, Optional[User]]:
        """用户登录"""
        user = self.data_manager.find_user_by_username(username)
        if not user:
            return False, "用户不存在", None

        hashed_password = self._hash_password(password)
        if user.password != hashed_password:
            return False, "密码错误", None

        if user.is_lost:
            return False, "账户已挂失，请联系银行", None

        if user.is_frozen:
            return False, "账户已冻结，请联系银行", None

        return True, "登录成功", user

    def get_user_info(self, user_id: str) -> Optional[User]:
        """获取用户信息"""
        return self.data_manager.find_user_by_id(user_id)

    def update_user_info(self, user: User) -> tuple[bool, str]:
        """更新用户信息"""
        if self.data_manager.update_user(user):
            return True, "信息更新成功"
        else:
            return False, "信息更新失败"