#!/usr/bin/env python
"""
Django的命令行管理工具，用于执行管理任务。

该脚本是Django项目的入口点，支持多种管理命令，如：
- runserver: 启动开发服务器
- migrate: 执行数据库迁移
- createsuperuser: 创建超级用户
- shell: 启动交互式Python shell
"""

# 导入操作系统模块
import os
# 导入系统模块
import sys


def main():
    """
    主函数，执行Django管理命令。
    设置Django配置模块环境变量，然后执行命令行参数指定的管理任务。
    """
    # 设置Django配置模块环境变量，指定项目的settings文件
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
    
    try:
        # 导入Django管理命令执行函数
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # 如果导入失败，抛出详细的错误信息
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # 执行命令行传入的管理命令
    execute_from_command_line(sys.argv)


# 如果脚本直接运行，调用主函数
if __name__ == '__main__':
    main()