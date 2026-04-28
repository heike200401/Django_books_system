# 导入Django管理后台模块
from django.contrib import admin
# 导入自定义的模型类
from .models import Book, Reader, BorrowRecord


# 注册图书模型到管理后台
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    图书管理后台配置类
    """
    # 列表页显示的字段
    list_display = ['isbn', 'title', 'author', 'publisher', 'category', 'total_quantity', 'available_quantity']
    # 可筛选的字段
    list_filter = ['category', 'publisher']
    # 可搜索的字段
    search_fields = ['isbn', 'title', 'author']
    # 每页显示20条记录
    list_per_page = 20


# 注册读者模型到管理后台
@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    """
    读者管理后台配置类
    """
    # 列表页显示的字段
    list_display = ['user', 'phone', 'max_borrow_count', 'current_borrow_count', 'created_at']
    # 可筛选的字段
    list_filter = ['created_at']
    # 可搜索的字段（支持跨表搜索）
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone']
    # 每页显示20条记录
    list_per_page = 20


# 注册借阅记录模型到管理后台
@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    """
    借阅记录管理后台配置类
    """
    # 列表页显示的字段
    list_display = ['book', 'reader', 'borrow_date', 'due_date', 'return_date', 'status', 'fine']
    # 可筛选的字段
    list_filter = ['status', 'borrow_date', 'due_date']
    # 可搜索的字段（支持跨表搜索）
    search_fields = ['book__title', 'reader__user__username']
    # 每页显示20条记录
    list_per_page = 20
    # 按日期分层显示
    date_hierarchy = 'borrow_date'