"""
ASGI config for library_system project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

# 导入操作系统模块
import os

# 导入Django的ASGI应用获取函数
from django.core.asgi import get_asgi_application

# 设置Django配置模块环境变量，指定项目的settings文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')

# 创建ASGI应用实例，供ASGI服务器（如Daphne、Uvicorn）使用
application = get_asgi_application()