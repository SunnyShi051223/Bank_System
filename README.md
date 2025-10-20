# 银行卡管理系统

这是一个基于Python开发的银行卡管理系统，包含用户管理、存取款管理和账户管理三大核心功能模块。

## 功能特性

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
- 账户冻结/解冻

## 项目结构

```
Bank/
├── app.py              # 主程序入口
├── README.md           # 项目说明
├── PROJECT_STRUCTURE.md # 项目结构说明
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

## 安装与运行

1. 确保已安装Python 3.6或更高版本
2. 克隆或下载本项目
3. 在项目根目录下运行以下命令启动系统：
   ```
   python app.py
   ```

## 使用说明

1. 首次使用需要注册账户
2. 注册完成后可以登录系统
3. 登录后可以进行存款、取款、查询余额等操作
4. 在账户管理中可以进行挂失、冻结、解冻、销户等操作

## 数据存储

系统使用JSON文件存储用户数据，默认存储在 `data/users.json` 文件中。

## 文档结构

- [README.md](README.md) - 项目说明
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 项目结构说明
- [REQUIREMENTS.md](REQUIREMENTS.md) - 系统需求规格说明
- [VERIFICATION.md](VERIFICATION.md) - 系统功能验证报告

## 注意事项

- 密码经过SHA256加密存储，保证安全性
- 挂失和销户操作不可逆，请谨慎操作
- 被挂失或冻结的账户无法进行交易操作
