# 银行卡管理系统项目结构

## 目录结构
```
Bank/
├── app.py              # 主程序入口
├── README.md           # 项目说明
├── PROJECT_STRUCTURE.md # 项目结构说明
├── REQUIREMENTS.md     # 系统需求规格说明
├── models/             # 数据模型
│   ├── __init__.py
│   └── user.py         # 用户模型
├── services/           # 业务逻辑层
│   ├── __init__.py
│   ├── user_service.py # 用户管理服务
│   ├── account_service.py # 账户管理服务
│   └── transaction_service.py # 交易服务
├── utils/              # 工具类
│   ├── __init__.py
│   └── data_manager.py # 数据管理工具
└── data/               # 数据存储目录
    └── users.json      # 用户数据文件
```

## 功能模块说明

### 1. 用户管理子系统
- 用户注册
- 用户登录
- 用户信息管理

### 2. 存取款管理子系统
- 存款
- 取款
- 查询余额

### 3. 账户管理子系统
- 挂失
- 销户
- 账户冻结