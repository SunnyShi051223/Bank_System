import sys
from services.user_service import UserService
from services.account_service import AccountService
from services.transaction_service import TransactionService
from models.user import User


class BankSystem:
    def __init__(self):
        self.user_service = UserService()
        self.account_service = AccountService()
        self.transaction_service = TransactionService()
        self.current_user = None

    def main_menu(self):
        """主菜单"""
        while True:
            print("\n" + "="*50)
            print("         银行卡管理系统")
            print("="*50)
            if self.current_user:
                print(f"欢迎，{self.current_user.username}！")
                print("1. 存款")
                print("2. 取款")
                print("3. 查询余额")
                print("4. 账户管理")
                print("5. 用户信息管理")
                print("6. 退出登录")
                print("0. 退出系统")
            else:
                print("1. 用户注册")
                print("2. 用户登录")
                print("0. 退出系统")
            
            choice = input("请选择操作: ").strip()
            
            if self.current_user:
                self._logged_in_menu(choice)
            else:
                self._logged_out_menu(choice)

    def _logged_out_menu(self, choice):
        """未登录状态菜单"""
        if choice == "1":
            self.register()
        elif choice == "2":
            self.login()
        elif choice == "0":
            print("感谢使用银行卡管理系统，再见！")
            sys.exit(0)
        else:
            print("无效选择，请重新输入！")

    def _logged_in_menu(self, choice):
        """已登录状态菜单"""
        if choice == "1":
            self.deposit()
        elif choice == "2":
            self.withdraw()
        elif choice == "3":
            self.check_balance()
        elif choice == "4":
            self.account_management()
        elif choice == "5":
            self.user_info_management()
        elif choice == "6":
            self.logout()
        elif choice == "0":
            print("感谢使用银行卡管理系统，再见！")
            sys.exit(0)
        else:
            print("无效选择，请重新输入！")

    def register(self):
        """用户注册"""
        print("\n--- 用户注册 ---")
        username = input("请输入用户名: ").strip()
        if not username:
            print("用户名不能为空！")
            return
            
        password = input("请输入密码: ").strip()
        if not password:
            print("密码不能为空！")
            return
            
        success, message = self.user_service.register(username, password)
        print(message)

    def login(self):
        """用户登录"""
        print("\n--- 用户登录 ---")
        username = input("请输入用户名: ").strip()
        if not username:
            print("用户名不能为空！")
            return
            
        password = input("请输入密码: ").strip()
        if not password:
            print("密码不能为空！")
            return
            
        success, message, user = self.user_service.login(username, password)
        print(message)
        if success:
            self.current_user = user

    def logout(self):
        """退出登录"""
        if self.current_user:
            print(f"用户 {self.current_user.username} 已退出登录")
            self.current_user = None

    def deposit(self):
        """存款"""
        print("\n--- 存款 ---")
        try:
            amount = float(input("请输入存款金额: "))
            success, message, balance = self.transaction_service.deposit(self.current_user, amount)
            print(message)
            if success:
                print(f"当前余额: {balance}")
        except ValueError:
            print("请输入有效的金额！")

    def withdraw(self):
        """取款"""
        print("\n--- 取款 ---")
        try:
            amount = float(input("请输入取款金额: "))
            success, message, balance = self.transaction_service.withdraw(self.current_user, amount)
            print(message)
            if success:
                print(f"当前余额: {balance}")
        except ValueError:
            print("请输入有效的金额！")

    def check_balance(self):
        """查询余额"""
        print("\n--- 查询余额 ---")
        success, message, balance = self.transaction_service.check_balance(self.current_user)
        print(message)
        print(f"当前余额: {balance}")

    def user_info_management(self):
        """用户信息管理"""
        while True:
            print("\n--- 用户信息管理 ---")
            print("1. 查看个人信息")
            print("2. 修改密码")
            print("0. 返回上级菜单")
            
            choice = input("请选择操作: ").strip()
            
            if choice == "1":
                self.view_user_info()
                break
            elif choice == "2":
                self.change_password()
                break
            elif choice == "0":
                break
            else:
                print("无效选择，请重新输入！")

    def view_user_info(self):
        """查看个人信息"""
        print("\n--- 个人信息 ---")
        print(f"用户名: {self.current_user.username}")
        print(f"账户状态: {'正常' if not self.current_user.is_frozen else '已冻结'}")
        print(f"账户余额: {self.current_user.balance}")
        print(f"注册时间: {self.current_user.created_at}")
        if self.current_user.is_lost:
            print("账户状态: 已挂失")

    def change_password(self):
        """修改密码"""
        print("\n--- 修改密码 ---")
        old_password = input("请输入原密码: ").strip()
        if not old_password:
            print("密码不能为空！")
            return
            
        # 验证原密码
        success, message, user = self.user_service.login(
            self.current_user.username, old_password)
        if not success:
            print(f"原密码{message}")
            return
            
        new_password = input("请输入新密码: ").strip()
        if not new_password:
            print("新密码不能为空！")
            return
            
        confirm_password = input("请再次输入新密码: ").strip()
        if new_password != confirm_password:
            print("两次输入的密码不一致！")
            return
            
        # 更新密码
        self.current_user.password = self.user_service._hash_password(new_password)
        success, message = self.user_service.update_user_info(self.current_user)
        print(message)

    def account_management(self):
        """账户管理"""
        while True:
            print("\n--- 账户管理 ---")
            print("1. 挂失账户")
            print("2. 冻结账户")
            print("3. 解冻账户")
            print("4. 销户")
            print("0. 返回上级菜单")
            
            choice = input("请选择操作: ").strip()
            
            if choice == "1":
                self.report_loss()
                break
            elif choice == "2":
                self.freeze_account()
                break
            elif choice == "3":
                self.unfreeze_account()
                break
            elif choice == "4":
                self.close_account()
                break
            elif choice == "0":
                break
            else:
                print("无效选择，请重新输入！")

    def report_loss(self):
        """挂失账户"""
        confirm = input("确定要挂失账户吗？此操作不可逆！(y/N): ").strip().lower()
        if confirm == "y":
            success, message = self.account_service.report_loss(self.current_user)
            print(message)
            if success:
                self.current_user = None  # 挂失后自动退出登录
        else:
            print("操作已取消")

    def freeze_account(self):
        """冻结账户"""
        confirm = input("确定要冻结账户吗？(y/N): ").strip().lower()
        if confirm == "y":
            success, message = self.account_service.freeze_account(self.current_user)
            print(message)
        else:
            print("操作已取消")

    def unfreeze_account(self):
        """解冻账户"""
        confirm = input("确定要解冻账户吗？(y/N): ").strip().lower()
        if confirm == "y":
            success, message = self.account_service.unfreeze_account(self.current_user)
            print(message)
        else:
            print("操作已取消")

    def close_account(self):
        """销户"""
        print("警告：销户将永久删除您的账户信息！")
        confirm = input("确定要销户吗？此操作不可逆！(y/N): ").strip().lower()
        if confirm == "y":
            password = input("请输入密码确认: ").strip()
            # 验证密码
            success, message, user = self.user_service.login(
                self.current_user.username, password)
            if success:
                success, message = self.account_service.close_account(self.current_user)
                print(message)
                if success:
                    self.current_user = None  # 销户后自动退出登录
            else:
                print("密码错误，销户失败！")
        else:
            print("操作已取消")


def main():
    bank_system = BankSystem()
    bank_system.main_menu()


if __name__ == "__main__":
    main()