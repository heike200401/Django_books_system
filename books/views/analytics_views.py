# 导入Django快捷函数
from django.shortcuts import render
# 导入Django ORM聚合函数
from django.db.models import Count, Sum, Q
# 导入Django时间工具
from django.utils import timezone
# 导入日期时间计算工具
from datetime import timedelta
# 导入相关模型
from ..models import Book, Reader, BorrowRecord


def dashboard(request):
    """
    仪表板视图函数，展示图书馆统计数据
    :param request: HTTP请求对象
    :return: 渲染仪表板页面，包含各类统计数据
    """
    # 统计图书总数
    total_books = Book.objects.count()
    # 统计读者总数
    total_readers = Reader.objects.count()
    # 统计借阅记录总数
    total_borrows = BorrowRecord.objects.count()
    # 统计当前借阅中数量
    current_borrows = BorrowRecord.objects.filter(status='borrowed').count()
    
    # 获取今天日期
    today = timezone.now().date()
    # 计算一周前日期
    week_ago = today - timedelta(days=7)
    # 计算一个月前日期
    month_ago = today - timedelta(days=30)
    
    # 统计本周借阅数量
    weekly_borrows = BorrowRecord.objects.filter(borrow_date__date__gte=week_ago).count()
    # 统计本月借阅数量
    monthly_borrows = BorrowRecord.objects.filter(borrow_date__date__gte=month_ago).count()
    
    # 统计逾期未还数量（状态为借阅中且应还日期已过）
    overdue_records = BorrowRecord.objects.filter(
        status='borrowed',
        due_date__lt=timezone.now()
    ).count()
    
    # 按分类统计图书数量和可借数量
    category_stats = Book.objects.values('category').annotate(
        count=Count('id'),
        total_available=Sum('available_quantity')
    )
    
    # 获取借阅次数最多的前10本图书
    popular_books = Book.objects.annotate(
        borrow_count=Count('borrow_records')
    ).order_by('-borrow_count')[:10]
    
    # 获取借阅次数最多的前10位读者
    active_readers = Reader.objects.annotate(
        borrow_count=Count('borrow_records')
    ).order_by('-borrow_count')[:10]
    
    # 准备上下文数据
    context = {
        'total_books': total_books,           # 图书总数
        'total_readers': total_readers,       # 读者总数
        'total_borrows': total_borrows,       # 借阅记录总数
        'current_borrows': current_borrows,   # 当前借阅数量
        'weekly_borrows': weekly_borrows,     # 本周借阅数量
        'monthly_borrows': monthly_borrows,   # 本月借阅数量
        'overdue_records': overdue_records,   # 逾期未还数量
        'category_stats': category_stats,     # 分类统计
        'popular_books': popular_books,       # 热门图书
        'active_readers': active_readers,     # 活跃读者
    }
    
    # 渲染仪表板模板并传递数据
    return render(request, 'analytics/dashboard.html', context)