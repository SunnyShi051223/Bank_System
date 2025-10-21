import json
import os
from typing import List, Dict, Optional
from models.user import User


class DataManager:
    def __init__(self, data_file: str = "data/users.json"):
        self.data_file = data_file
        # 确保数据目录存在
        os.makedirs(os.path.dirname(data_file), exist_ok=True)
        # 如果数据文件不存在，创建一个空的
        if not os.path.exists(data_file):
            self._create_empty_data_file()

    def _create_empty_data_file(self) -> None:
        """创建空的数据文件"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)

    def load_users(self) -> List[User]:
        """从文件加载所有用户"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [User.from_dict(user_data) for user_data in data]
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def save_users(self, users: List[User]) -> bool:
        """保存用户列表到文件"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([user.to_dict() for user in users], f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存用户数据时出错: {e}")
            return False

    def find_user_by_username(self, username: str) -> Optional[User]:
        """根据用户名查找用户"""
        users = self.load_users()
        for user in users:
            if user.username == username:
                return user
        return None

    def find_user_by_id(self, user_id: str) -> Optional[User]:
        """根据用户ID查找用户"""
        users = self.load_users()
        for user in users:
            if user.user_id == user_id:
                return user
        return None

    def add_user(self, user: User) -> bool:
        """添加新用户"""
        users = self.load_users()
        # 检查用户名是否已存在
        if self.find_user_by_username(user.username):
            return False
        users.append(user)
        return self.save_users(users)

    def update_user(self, user: User) -> bool:
        """更新用户信息"""
        users = self.load_users()
        for i, u in enumerate(users):
            if u.user_id == user.user_id:
                users[i] = user
                return self.save_users(users)
        return False

    def delete_user(self, user_id: str) -> bool:
        """删除用户"""
        users = self.load_users()
        updated_users = [u for u in users if u.user_id != user_id]
        if len(updated_users) == len(users):
            # 没有删除任何用户
            return False
        return self.save_users(updated_users)