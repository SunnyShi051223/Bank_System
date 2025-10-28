import json
from datetime import datetime
from typing import Optional


class User:
    def __init__(self, user_id: str, username: str, password: str, balance: float = 0.0,
                 is_frozen: bool = False, is_lost: bool = False, is_using = False):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.balance = balance
        self.is_frozen = is_frozen
        self.is_lost = is_lost
        self.created_at = datetime.now().isoformat()
        self.is_using = is_using

    def to_dict(self) -> dict:
        """将用户对象转换为字典"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password": self.password,
            "balance": self.balance,
            "is_frozen": self.is_frozen,
            "is_lost": self.is_lost,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """从字典创建用户对象"""
        user = cls(
            data["user_id"],
            data["username"],
            data["password"],
            data.get("balance", 0.0),
            data.get("is_frozen", False),
            data.get("is_lost", False)
        )
        user.created_at = data.get("created_at", datetime.now().isoformat())
        return user

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