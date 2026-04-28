# 导入操作系统模块
import os
# 导入Django模块
import django

# 设置Django配置模块环境变量，指定项目的settings文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
# 初始化Django环境
django.setup()

# 导入Django内置用户模型
from django.contrib.auth.models import User

# 超级用户配置信息
username = 'admin'
password = 'admin123'
email = 'admin@example.com'

# 检查超级用户是否已存在
if not User.objects.filter(username=username).exists():
    # 创建超级用户
    User.objects.create_superuser(username=username, password=password, email=email)
    # 输出创建成功信息
    print(f'超级用户 {username} 创建成功！')
    print(f'用户名: {username}')
    print(f'密码: {password}')
else:
    # 如果用户已存在，输出提示信息
    print(f'超级用户 {username} 已存在！')