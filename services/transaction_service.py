from typing import Optional
from models.user import User
from utils.data_manager import DataManager


class TransactionService:
    def __init__(self):
        self.data_manager = DataManager()

    def deposit(self, user: User, amount: float) -> tuple[bool, str, float]:
        """存款"""
        if user.is_lost:
            return False, "账户已挂失，无法进行交易", user.balance
        if user.is_frozen:
            return False, "账户已冻结，无法进行交易", user.balance

        if user.deposit(amount):
            if self.data_manager.update_user(user):
                return True, f"存款成功，存入金额: {amount}", user.balance
            else:
                # 回滚操作
                user.withdraw(amount)
                return False, "存款失败，请稍后重试", user.balance
        else:
            return False, "存款金额必须大于0", user.balance

    def withdraw(self, user: User, amount: float) -> tuple[bool, str, float]:
        """取款"""
        if user.is_lost:
            return False, "账户已挂失，无法进行交易", user.balance
        if user.is_frozen:
            return False, "账户已冻结，无法进行交易", user.balance

        if amount <= 0:
            return False, "取款金额必须大于0", user.balance

        if amount > user.balance:
            return False, "余额不足", user.balance

        if user.withdraw(amount):
            if self.data_manager.update_user(user):
                return True, f"取款成功，取出金额: {amount}", user.balance
            else:
                # 回滚操作
                user.deposit(amount)
                return False, "取款失败，请稍后重试", user.balance
        else:
            return False, "取款失败", user.balance

    def check_balance(self, user: User) -> tuple[bool, str, float]:
        """查询余额"""
        return True, "查询成功", user.check_balance()