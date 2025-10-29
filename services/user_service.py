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

    def login(self, username: str, password: str) -> tuple[bool, str, Optional[User], Optional[str]]:
        """
        用户登录
        返回: (success, message, user, session_token)
        """
        user = self.data_manager.find_user_by_username(username)
        if not user:
            return False, "用户不存在", None, None

        # 检查是否已登录
        if user.is_using and user.session_token:
            return False, "该账户已在其他设备登录", None, None

        hashed_password = self._hash_password(password)
        if user.password != hashed_password:
            return False, "密码错误", None, None

        if user.is_lost:
            return False, "账户已挂失，请联系银行", None, None

        if user.is_frozen:
            return False, "账户已冻结，请联系银行", None, None

        # 生成新的会话令牌
        session_token = user.generate_session_token()
        if not self.data_manager.update_user(user):
            return False, "登录失败，请稍后重试", None, None
            
        return True, "登录成功", user, session_token

    def get_user_info(self, user_id: str) -> Optional[User]:
        """获取用户信息"""
        return self.data_manager.find_user_by_id(user_id)

    def update_user_info(self, user: User) -> tuple[bool, str]:
        """更新用户信息"""
        if self.data_manager.update_user(user):
            return True, "信息更新成功"
        else:
            return False, "信息更新失败"
            
    def logout(self, user: User) -> tuple[bool, str]:
        """用户登出"""
        if not user or not user.is_using:
            return False, "用户未登录"
            
        user.clear_session()
        if self.data_manager.update_user(user):
            return True, "登出成功"
        return False, "登出失败，请稍后重试"
        
    def validate_session(self, user_id: str, session_token: str) -> tuple[bool, Optional[User]]:
        """验证用户会话是否有效"""
        user = self.data_manager.find_user_by_id(user_id)
        if not user or not user.is_session_valid(session_token):
            return False, None
        return True, user