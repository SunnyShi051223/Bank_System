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
        self.clear_window()
        frame = tk.Frame(self.root, bg="#f0f4f8")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(frame, text="用户登录", font=("微软雅黑", 22, "bold"), fg="#2d4059", bg="#f0f4f8").pack(pady=30)
        form_frame = tk.Frame(frame, bg="#f0f4f8")
        form_frame.pack(pady=10)
        tk.Label(form_frame, text="用户名：", font=("微软雅黑", 14), bg="#f0f4f8").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        username_entry = tk.Entry(form_frame, font=("微软雅黑", 14), width=20)
        username_entry.grid(row=0, column=1, padx=10, pady=10)
        tk.Label(form_frame, text="密码：", font=("微软雅黑", 14), bg="#f0f4f8").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        password_entry = tk.Entry(form_frame, font=("微软雅黑", 14), width=20, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=10)

        def do_login():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            if not username or not password:
                messagebox.showwarning("提示", "用户名和密码不能为空！")
                return
            success, message, user, session_token = self.user_service.login(username, password)
            if success:
                self.current_user = user
                self.current_session_token = session_token
                messagebox.showinfo("登录成功", message)
                self.user_menu()
            else:
                messagebox.showerror("登录失败", message)

        btn_style = {"font": ("微软雅黑", 13), "bg": "#30a7e1", "fg": "white", "activebackground": "#1976d2", "activeforeground": "#fff", "relief": "groove", "bd": 2, "width": 12, "height": 2}
        btn_frame = tk.Frame(frame, bg="#f0f4f8")
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="登录", command=do_login, **btn_style).grid(row=0, column=0, padx=20)
        tk.Button(btn_frame, text="返回主页", command=self.main_menu, **btn_style).grid(row=0, column=1, padx=20)

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
        self.clear_window()
        frame = tk.Frame(self.root, bg="#f0f4f8")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(frame, text="存款", font=("微软雅黑", 22, "bold"), fg="#2d4059", bg="#f0f4f8").pack(pady=30)
        tk.Label(frame, text="请输入存款金额：", font=("微软雅黑", 14), bg="#f0f4f8").pack(pady=10)
        amount_entry = tk.Entry(frame, font=("微软雅黑", 14), width=20)
        amount_entry.pack(pady=10)
        result_label = tk.Label(frame, text="", font=("微软雅黑", 13), fg="#1976d2", bg="#f0f4f8")
        result_label.pack(pady=10)
        def do_deposit():
            try:
                amount = float(amount_entry.get())
            except ValueError:
                result_label.config(text="请输入有效的金额！", fg="red")
                return
            success, message, balance = self.transaction_service.deposit(self.current_user, amount)
            if success:
                result_label.config(text=f"{message}\n当前余额：{balance:.2f}", fg="#1976d2")
            else:
                result_label.config(text=message, fg="red")
        btn_style = {"font": ("微软雅黑", 13), "bg": "#30a7e1", "fg": "white", "activebackground": "#1976d2", "activeforeground": "#fff", "relief": "groove", "bd": 2, "width": 12, "height": 2}
        btn_frame = tk.Frame(frame, bg="#f0f4f8")
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="确认存款", command=do_deposit, **btn_style).grid(row=0, column=0, padx=20)
        tk.Button(btn_frame, text="返回菜单", command=self.user_menu, **btn_style).grid(row=0, column=1, padx=20)

    def withdraw(self):
        self.clear_window()
        frame = tk.Frame(self.root, bg="#f0f4f8")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(frame, text="取款", font=("微软雅黑", 22, "bold"), fg="#2d4059", bg="#f0f4f8").pack(pady=30)
        tk.Label(frame, text="请输入取款金额：", font=("微软雅黑", 14), bg="#f0f4f8").pack(pady=10)
        amount_entry = tk.Entry(frame, font=("微软雅黑", 14), width=20)
        amount_entry.pack(pady=10)
        result_label = tk.Label(frame, text="", font=("微软雅黑", 13), fg="#1976d2", bg="#f0f4f8")
        result_label.pack(pady=10)
        def do_withdraw():
            try:
                amount = float(amount_entry.get())
            except ValueError:
                result_label.config(text="请输入有效的金额！", fg="red")
                return
            success, message, balance = self.transaction_service.withdraw(self.current_user, amount)
            if success:
                result_label.config(text=f"{message}\n当前余额：{balance:.2f}", fg="#1976d2")
            else:
                result_label.config(text=message, fg="red")
        btn_style = {"font": ("微软雅黑", 13), "bg": "#30a7e1", "fg": "white", "activebackground": "#1976d2", "activeforeground": "#fff", "relief": "groove", "bd": 2, "width": 12, "height": 2}
        btn_frame = tk.Frame(frame, bg="#f0f4f8")
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="确认取款", command=do_withdraw, **btn_style).grid(row=0, column=0, padx=20)
        tk.Button(btn_frame, text="返回菜单", command=self.user_menu, **btn_style).grid(row=0, column=1, padx=20)

    def check_balance(self):
        self.clear_window()
        frame = tk.Frame(self.root, bg="#f0f4f8")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(frame, text="查询余额", font=("微软雅黑", 22, "bold"), fg="#2d4059", bg="#f0f4f8").pack(pady=30)
        success, message, balance = self.transaction_service.check_balance(self.current_user)
        if success:
            info = f"{message}\n当前余额：{balance:.2f}"
            fg = "#1976d2"
        else:
            info = message
            fg = "red"
        tk.Label(frame, text=info, font=("微软雅黑", 15), fg=fg, bg="#f0f4f8").pack(pady=30)
        btn_style = {"font": ("微软雅黑", 13), "bg": "#30a7e1", "fg": "white", "activebackground": "#1976d2", "activeforeground": "#fff", "relief": "groove", "bd": 2, "width": 12, "height": 2}
        tk.Button(frame, text="返回菜单", command=self.user_menu, **btn_style).pack(pady=20)

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
