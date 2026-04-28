# 导入Django应用配置基类
from django.apps import AppConfig


class LibraryConfig(AppConfig):
    """
    library应用的配置类
    """
    # 应用名称，用于Django识别该应用
    name = 'library'