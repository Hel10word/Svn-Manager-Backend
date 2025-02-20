## SVN Manager

一个基于 Python + FastAPI 构建的现代化 SVN 文件管理系统。本项目只是后端 , 对应的前端项目 : [Svn-Manager-Frontend](https://github.com/Hel10word/Svn-Manager-Frontend)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)  [![FastAPI](https://img.shields.io/badge/FastAPI-0.112.0-green)](https://fastapi.tiangolo.com/)  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)



## 功能特点

基于 FastAPI 的 SVN 管理系统后端服务，提供了 SVN 文件锁定管理、日志查看等功能的 RESTful API 接口。

- 🔐 SVN 账号认证与登录
- 🔒 文件锁定管理
  - 查看文件锁定状态
  - 锁定/解锁文件
  - 批量操作支持
- 📝 SVN 日志查看
  - 支持多路径日志查询
  - 提交记录详情展示
- 🛡️ JWT Token 认证
- 🎯 统一异常处理
- 📊 日志记录与管理



## 开始使用

### 环境要求

- Python 3.8+
- SVN 命令行工具

### 安装

```bash
# 进入项目目录
cd Svn-Manager-Backend
# 复制配置模板
cp config/env.yaml.template config/env.yaml
## 根据相关的需求 修改配置文件 , 然后便可启动
```

### 启动

```bash
################## windows 环境启动
# 直接运行 bat 脚本
call start.bat

################## Linux 环境启动
# 创建并激活虚拟环境
python -m venv venv
# 加载 Python 虚拟环境 
source venv/bin/activate
# 安装依赖
pip install -r requirements.txt
# 启动
python run.py
```



## 项目结构

```bash
Svn-Manager-Backend/
├── config/ # 配置文件目录
├── src/ # 源代码目录
│ ├── fastapi/ # FastAPI 相关代码
│ │ ├── api/ # API 接口定义
│ │ ├── handler/ # 异常处理器
│ │ └── module/ # 数据模型
│ ├── manager/ # 管理器模块
│ ├── module/ # 核心模块
│ └── util/ # 工具类
├── requirements.txt # 项目依赖
├── run.py # 启动文件
└── start.bat # Windows 启动脚本
```



## API 接口

### 认证相关
- `POST /login` - 用户登录
- `POST /logout` - 用户登出

### SVN 操作
- `GET /svn/svn-data/` - 获取文件锁定状态
- `POST /svn/svn-lock/` - 锁定文件
- `POST /svn/svn-unlock/` - 解锁文件
- `POST /svn/svn-log/` - 查看 SVN 日志



## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request
