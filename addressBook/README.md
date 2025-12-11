# 📇 Flask 地址簿管理系统

一个功能完整的在线地址簿应用，基于 Flask 框架开发，支持联系人管理、收藏功能、Excel 导入导出等。

![Flask](https://img.shields.io/badge/Flask-3.1.2-blue)
![Python](https://img.shields.io/badge/Python-3.10-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)


## 🌐 在线演示
**访问地址：** https://liyuxin.pythonanywhere.com

## ✨ 功能特性

### 📋 核心功能
- ✅ **联系人管理**：完整的增删改查（CRUD）功能
- ✅ **星标收藏**：一键收藏重要联系人，置顶显示
- ✅ **多字段存储**：姓名、电话、邮箱、社交账号、地址、备注
- ✅ **响应式设计**：适配电脑、平板、手机等设备

### 📊 数据管理
- ✅ **Excel 导出**：一键导出所有联系人为 Excel 文件
- ✅ **Excel 导入**：批量导入联系人数据
- ✅ **数据持久化**：SQLite 数据库存储
- ✅ **数据备份**：随时导出备份

### 🎨 用户界面
- ✅ **现代化设计**：渐变背景、卡片式布局
- ✅ **图标化操作**：Font Awesome 图标集
- ✅ **即时反馈**：操作成功/失败提示
- ✅ **三栏布局**：添加、浏览、导入导出分区明确

## 📁 项目结构
- `app.py` - Flask 主程序  
- `requirements.txt` - 依赖列表  
- `static/style.css` - 样式文件  
- `templates/index.html` - 主页面  
- `templates/edit_contact.html` - 编辑页面

## 🛠️ 技术栈

| 技术 | 用途 | 版本 |
|------|------|------|
| **Python** | 后端语言 | 3.10+ |
| **Flask** | Web 框架 | 3.1.2 |
| **Flask-SQLAlchemy** | ORM 数据库 | 3.1.1 |
| **SQLite** | 数据库 | 3.35+ |
| **Pandas** | Excel 处理 | 2.0.3 |
| **OpenPyXL** | Excel 读写 | 3.1.2 |
| **HTML/CSS/JS** | 前端界面 | - |
| **Font Awesome** | 图标库 | 6.4.0 |

## 🚀 快速开始

### 环境要求
- Python 3.10 或更高版本
- pip 包管理器

### 安装依赖
```bash
pip install flask flask-sqlalchemy pandas openpyxl