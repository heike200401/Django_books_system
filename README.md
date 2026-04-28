# 图书管理系统

基于 Django 6.0 的图书管理系统，提供图书管理、读者管理、借阅管理和数据分析功能。

## 功能特性

- **图书管理**：图书的增删改查，支持分类管理、封面上传
- **读者管理**：读者信息管理，支持借阅限额设置
- **借阅管理**：借阅登记、归还处理、逾期管理、罚金计算
- **数据分析**：借阅统计、热门图书排行等可视化报表

## 技术栈

- **框架**: Django 6.0.4
- **数据库**: MySQL 5.7+ / SQLite（开发环境）
- **数据分析**: pandas 3.0 + matplotlib 3.10
- **语言**: Python 3.10+

## 项目结构

```
Django_books_system/
├── books/                    # 核心应用
│   ├── views/               # 视图模块
│   │   ├── book_views.py    # 图书管理视图
│   │   ├── reader_views.py  # 读者管理视图
│   │   ├── borrow_views.py  # 借阅管理视图
│   │   └── analytics_views.py # 数据分析视图
│   ├── models.py            # 数据模型
│   ├── urls.py              # 路由配置
│   ├── admin.py             # 后台管理
│   └── templates/           # 模板文件
├── library_system/          # 项目配置
│   ├── settings.py          # 配置文件
│   ├── urls.py              # 根路由
│   └── wsgi.py              # WSGI入口
├── manage.py                # Django管理命令
├── requirements.txt         # 依赖列表
└── db.sqlite3               # SQLite数据库（开发）
```

## 快速开始

### 环境要求

- Python 3.10+
- MySQL 5.7+ 或 SQLite（开发环境）

### 安装依赖

```bash
pip install -r requirements.txt
```

### 数据库配置

1. 创建 MySQL 数据库：
```sql
CREATE DATABASE library CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 修改 `library_system/settings.py` 中的数据库配置：
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'library',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 创建超级用户

```bash
python manage.py createsuperuser
```

或使用脚本：
```bash
python create_superuser.py
```

### 生成测试数据

```bash
python manage.py generate_test_data
```

### 启动开发服务器

```bash
python manage.py runserver 0.0.0.0:8000
```

访问 http://localhost:8000 查看应用。

## 数据模型

### Book（图书）
| 字段 | 类型 | 说明 |
|------|------|------|
| isbn | CharField | ISBN编号（唯一） |
| title | CharField | 书名 |
| author | CharField | 作者 |
| publisher | CharField | 出版社 |
| publish_date | DateField | 出版日期 |
| category | CharField | 分类（文学/科学/技术/历史/哲学/艺术/其他） |
| price | DecimalField | 价格 |
| total_quantity | IntegerField | 总数量 |
| available_quantity | IntegerField | 可借数量 |
| description | TextField | 简介 |
| cover_image | ImageField | 封面图片 |

### Reader（读者）
| 字段 | 类型 | 说明 |
|------|------|------|
| user | OneToOneField | 关联用户 |
| phone | CharField | 联系电话 |
| address | CharField | 地址 |
| max_borrow_count | IntegerField | 最大借阅数（默认5） |
| current_borrow_count | IntegerField | 当前借阅数 |

### BorrowRecord（借阅记录）
| 字段 | 类型 | 说明 |
|------|------|------|
| book | ForeignKey | 关联图书 |
| reader | ForeignKey | 关联读者 |
| borrow_date | DateTimeField | 借阅日期 |
| due_date | DateTimeField | 应还日期 |
| return_date | DateTimeField | 归还日期 |
| status | CharField | 状态（借阅中/已归还/已逾期） |
| fine | DecimalField | 罚金 |

## 访问权限

- 管理员：完整权限，可访问管理后台
- 读者：可查看图书列表，查看个人借阅记录

## 许可证

MIT License