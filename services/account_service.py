from typing import Optional
from models.user import User
from utils.data_manager import DataManager


class AccountService:
    def __init__(self):
        self.data_manager = DataManager()

    def report_loss(self, user: User) -> tuple[bool, str]:
        """挂失账户"""
        user.report_loss()
        if self.data_manager.update_user(user):
            return True, "账户挂失成功"
        else:
            return False, "挂失失败，请稍后重试"

    def close_account(self, user: User) -> tuple[bool, str]:
        """销户"""
        if self.data_manager.delete_user(user.user_id):
            return True, "账户注销成功"
        else:
            return False, "销户失败，请稍后重试"

    def freeze_account(self, user: User) -> tuple[bool, str]:
        """冻结账户"""
        user.freeze_account()
        if self.data_manager.update_user(user):
            return True, "账户冻结成功"
        else:
            return False, "冻结失败，请稍后重试"

    def unfreeze_account(self, user: User) -> tuple[bool, str]:
        """解冻账户"""
        user.unfreeze_account()
        if self.data_manager.update_user(user):
            return True, "账户解冻成功"
        else:
            return False, "解冻失败，请稍后重试"