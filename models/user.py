import json
from datetime import datetime
from typing import Optional


class User:
    def __init__(self, user_id: str, username: str, password: str, balance: float = 0.0,
                 is_frozen: bool = False, is_lost: bool = False, is_using: bool = False,
                 session_token: str = None, last_login: str = None):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.balance = balance
        self.is_frozen = is_frozen
        self.is_lost = is_lost
        self.is_using = is_using
        self.session_token = session_token
        self.last_login = last_login if last_login else datetime.now().isoformat()
        self.created_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        """将用户对象转换为字典"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password": self.password,
            "balance": self.balance,
            "is_frozen": self.is_frozen,
            "is_lost": self.is_lost,
            "is_using": self.is_using,
            "session_token": self.session_token,
            "last_login": self.last_login,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """从字典创建用户对象"""
        user = cls(
            user_id=data["user_id"],
            username=data["username"],
            password=data["password"],
            balance=data.get("balance", 0.0),
            is_frozen=data.get("is_frozen", False),
            is_lost=data.get("is_lost", False),
            is_using=data.get("is_using", False),
            session_token=data.get("session_token"),
            last_login=data.get("last_login")
        )
        user.created_at = data.get("created_at", datetime.now().isoformat())
        return user

    def generate_session_token(self) -> str:
        """生成新的会话令牌"""
        import secrets
        self.session_token = secrets.token_hex(16)
        self.last_login = datetime.now().isoformat()
        self.is_using = True
        return self.session_token
        
    def clear_session(self) -> None:
        """清除会话信息"""
        self.session_token = None
        self.is_using = False
        
    def is_session_valid(self, token: str) -> bool:
        """验证会话令牌是否有效"""
        return self.session_token is not None and self.session_token == token and self.is_using
        
    def deposit(self, amount: float) -> bool:
        """存款"""
        if amount <= 0:
            return False
        self.balance += amount
        return True

    def withdraw(self, amount: float) -> bool:
        """取款"""
        if amount <= 0 or amount > self.balance:
            return False
        self.balance -= amount
        return True

    def check_balance(self) -> float:
        """查询余额"""
        return self.balance

    def report_loss(self) -> None:
        """挂失账户"""
        self.is_lost = True

    def unfreeze_account(self) -> None:
        """解冻账户"""
        self.is_frozen = False

    def freeze_account(self) -> None:
        """冻结账户"""
        self.is_frozen = True