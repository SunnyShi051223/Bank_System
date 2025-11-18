import tkinter as tk
from tkinter import messagebox, simpledialog
from services.user_service import UserService
from services.transaction_service import TransactionService
from services.account_service import AccountService

class BankGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("银行卡管理系统")
        self.root.geometry("1420x920")
        self.root.configure(bg="#f0f4f8")
        self.user_service = UserService()
        self.transaction_service = TransactionService()
        self.account_service = AccountService()
        self.current_user = None
        self.current_session_token = None
        self.main_menu()

    def main_menu(self):
        self.clear_window()
        frame = tk.Frame(self.root, bg="#f0f4f8")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(frame, text="银行卡管理系统", font=("微软雅黑", 22, "bold"), fg="#2d4059", bg="#f0f4f8").pack(pady=30)
        btn_style = {"font": ("微软雅黑", 13), "bg": "#30a7e1", "fg": "white", "activebackground": "#1976d2", "activeforeground": "#fff", "relief": "groove", "bd": 2, "width": 18, "height": 2}
        tk.Button(frame, text="用户登录", command=self.login, **btn_style).pack(pady=8)
        tk.Button(frame, text="用户注册", command=self.register, **btn_style).pack(pady=8)
        tk.Button(frame, text="退出系统", command=self.root.quit, **btn_style).pack(pady=8)

    def login(self):
        login_win = tk.Toplevel(self.root)
        login_win.title("用户登录")
        login_win.geometry("320x200")
        login_win.configure(bg="#f0f4f8")
        login_win.grab_set()
        tk.Label(login_win, text="用户名：", font=("微软雅黑", 12), bg="#f0f4f8").place(x=40, y=40)
        username_entry = tk.Entry(login_win, font=("微软雅黑", 12), width=18)
        username_entry.place(x=110, y=40)
        tk.Label(login_win, text="密码：", font=("微软雅黑", 12), bg="#f0f4f8").place(x=40, y=90)
        password_entry = tk.Entry(login_win, font=("微软雅黑", 12), width=18, show="*")
        password_entry.place(x=110, y=90)

        def do_login():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            if not username or not password:
                messagebox.showwarning("提示", "用户名和密码不能为空！", parent=login_win)
                return
            success, message, user, session_token = self.user_service.login(username, password)
            if success:
                self.current_user = user
                self.current_session_token = session_token
                messagebox.showinfo("登录成功", message, parent=login_win)
                login_win.destroy()
                self.user_menu()
            else:
                messagebox.showerror("登录失败", message, parent=login_win)

        btn_style = {"font": ("微软雅黑", 12), "bg": "#30a7e1", "fg": "white", "activebackground": "#1976d2", "activeforeground": "#fff", "relief": "groove", "bd": 2, "width": 10, "height": 1}
        tk.Button(login_win, text="登录", command=do_login, **btn_style).place(x=60, y=140)
        tk.Button(login_win, text="取消", command=login_win.destroy, **btn_style).place(x=170, y=140)

    def register(self):
        username = simpledialog.askstring("注册", "请输入用户名：")
        password = simpledialog.askstring("注册", "请输入密码：", show="*")
        confirm = simpledialog.askstring("注册", "请确认密码：", show="*")
        if not username or not password or not confirm:
            messagebox.showwarning("提示", "所有字段不能为空！")
            return
        if password != confirm:
            messagebox.showwarning("提示", "两次密码不一致！")
            return
        success, message = self.user_service.register(username, password)
        if success:
            messagebox.showinfo("注册成功", message)
        else:
            messagebox.showerror("注册失败", message)

    def user_menu(self):
        self.clear_window()
        frame = tk.Frame(self.root, bg="#f0f4f8")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(frame, text=f"欢迎，{self.current_user.username}！", font=("微软雅黑", 18, "bold"), fg="#2d4059", bg="#f0f4f8").pack(pady=25)
        btn_style = {"font": ("微软雅黑", 13), "bg": "#30a7e1", "fg": "white", "activebackground": "#1976d2", "activeforeground": "#fff", "relief": "groove", "bd": 2, "width": 18, "height": 2}
        tk.Button(frame, text="存款", command=self.deposit, **btn_style).pack(pady=6)
        tk.Button(frame, text="取款", command=self.withdraw, **btn_style).pack(pady=6)
        tk.Button(frame, text="查询余额", command=self.check_balance, **btn_style).pack(pady=6)
        tk.Button(frame, text="账户挂失", command=self.report_loss, **btn_style).pack(pady=6)
        tk.Button(frame, text="账户冻结", command=self.freeze_account, **btn_style).pack(pady=6)
        tk.Button(frame, text="账户解冻", command=self.unfreeze_account, **btn_style).pack(pady=6)
        tk.Button(frame, text="退出登录", command=self.logout, **btn_style).pack(pady=12)

    def deposit(self):
        amount = simpledialog.askfloat("存款", "请输入存款金额：")
        if amount is None:
            return
        success, message, balance = self.transaction_service.deposit(self.current_user, amount)
        if success:
            messagebox.showinfo("存款成功", f"{message}\n当前余额：{balance:.2f}")
        else:
            messagebox.showerror("存款失败", message)

    def withdraw(self):
        amount = simpledialog.askfloat("取款", "请输入取款金额：")
        if amount is None:
            return
        success, message, balance = self.transaction_service.withdraw(self.current_user, amount)
        if success:
            messagebox.showinfo("取款成功", f"{message}\n当前余额：{balance:.2f}")
        else:
            messagebox.showerror("取款失败", message)

    def check_balance(self):
        success, message, balance = self.transaction_service.check_balance(self.current_user)
        if success:
            messagebox.showinfo("余额", f"{message}\n当前余额：{balance:.2f}")
        else:
            messagebox.showerror("查询失败", message)

    def report_loss(self):
        if messagebox.askyesno("挂失", "确定要挂失账户吗？此操作不可逆！"):
            success, message = self.account_service.report_loss(self.current_user)
            if success:
                messagebox.showinfo("挂失成功", message)
                self.logout()
            else:
                messagebox.showerror("挂失失败", message)

    def freeze_account(self):
        if messagebox.askyesno("冻结", "确定要冻结账户吗？"):
            success, message = self.account_service.freeze_account(self.current_user)
            if success:
                messagebox.showinfo("冻结成功", message)
            else:
                messagebox.showerror("冻结失败", message)

    def unfreeze_account(self):
        if messagebox.askyesno("解冻", "确定要解冻账户吗？"):
            success, message = self.account_service.unfreeze_account(self.current_user)
            if success:
                messagebox.showinfo("解冻成功", message)
            else:
                messagebox.showerror("解冻失败", message)

    def logout(self):
        if self.current_user:
            self.user_service.logout(self.current_user)
        self.current_user = None
        self.current_session_token = None
        self.main_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BankGUI(root)
    root.mainloop()
