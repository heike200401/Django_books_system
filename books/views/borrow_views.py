# 导入Django快捷函数
from django.shortcuts import render, redirect, get_object_or_404
# 导入Django消息框架
from django.contrib import messages
# 导入Django时间工具
from django.utils import timezone
# 导入日期时间计算工具
from datetime import timedelta
# 导入相关模型
from ..models import BorrowRecord, Book, Reader
# 导入分页器
from django.core.paginator import Paginator


def borrow_list(request):
    """
    借阅记录列表视图函数
    :param request: HTTP请求对象
    :return: 渲染借阅记录列表页面
    """
    # 获取所有借阅记录对象
    records = BorrowRecord.objects.all()
    # 创建分页器，每页显示10条记录
    paginator = Paginator(records, 10)
    # 获取当前页码
    page = request.GET.get('page')
    # 获取当前页的借阅记录数据
    records_page = paginator.get_page(page)
    # 渲染模板并传递数据
    return render(request, 'borrows/borrow_list.html', {'records': records_page})


def borrow_detail(request, pk):
    """
    借阅记录详情视图函数
    :param request: HTTP请求对象
    :param pk: 借阅记录的主键ID
    :return: 渲染借阅记录详情页面
    """
    # 根据主键获取借阅记录对象，不存在则返回404
    record = get_object_or_404(BorrowRecord, pk=pk)
    # 渲染模板并传递借阅记录对象
    return render(request, 'borrows/borrow_detail.html', {'record': record})


def borrow_add(request):
    """
    添加借阅记录视图函数
    :param request: HTTP请求对象
    :return: GET请求返回表单页面，POST请求处理表单提交
    """
    # 判断是否为POST请求（表单提交）
    if request.method == 'POST':
        try:
            # 获取表单数据
            book_id = request.POST.get('book')
            reader_id = request.POST.get('reader')
            days = int(request.POST.get('borrow_days', 30))  # 默认借阅30天
            
            # 根据ID获取图书和读者对象
            book = get_object_or_404(Book, pk=book_id)
            reader = get_object_or_404(Reader, pk=reader_id)
            
            # 检查图书库存
            if book.available_quantity <= 0:
                messages.error(request, '该图书库存不足！')
                return redirect('borrow_add')
            
            # 检查读者借阅数量限制
            if reader.current_borrow_count >= reader.max_borrow_count:
                messages.error(request, '该读者已达最大借阅数量！')
                return redirect('borrow_add')
            
            # 计算应还日期（当前时间 + 借阅天数）
            due_date = timezone.now() + timedelta(days=days)
            
            # 创建借阅记录对象
            record = BorrowRecord(
                book=book,
                reader=reader,
                due_date=due_date
            )
            # 保存到数据库
            record.save()
            
            # 更新图书可借数量（减1）
            book.available_quantity -= 1
            book.save()
            
            # 更新读者当前借阅数量（加1）
            reader.current_borrow_count += 1
            reader.save()
            
            # 借阅成功提示消息
            messages.success(request, '借阅成功！')
            # 重定向到借阅记录列表页
            return redirect('borrow_list')
        except Exception as e:
            # 借阅失败提示消息
            messages.error(request, f'借阅失败：{str(e)}')
    
    # GET请求，获取可借阅的图书列表和所有读者列表
    books = Book.objects.filter(available_quantity__gt=0)
    readers = Reader.objects.all()
    # 渲染表单页面并传递数据
    return render(request, 'borrows/borrow_form.html', {'books': books, 'readers': readers})


def borrow_return(request, pk):
    """
    图书归还视图函数
    :param request: HTTP请求对象
    :param pk: 借阅记录的主键ID
    :return: GET请求返回归还确认页面，POST请求执行归还操作
    """
    # 根据主键获取借阅记录对象，不存在则返回404
    record = get_object_or_404(BorrowRecord, pk=pk)
    
    # 检查图书是否已归还
    if record.status == 'returned':
        messages.warning(request, '该图书已归还！')
        return redirect('borrow_list')
    
    # 判断是否为POST请求（确认归还）
    if request.method == 'POST':
        try:
            # 更新归还日期为当前时间
            record.return_date = timezone.now()
            # 更新状态为已归还
            record.status = 'returned'
            
            # 计算逾期罚金（逾期一天0.5元）
            if record.return_date > record.due_date:
                overdue_days = (record.return_date - record.due_date).days
                record.fine = overdue_days * 0.5
            
            # 保存借阅记录
            record.save()
            
            # 更新图书可借数量（加1）
            book = record.book
            book.available_quantity += 1
            book.save()
            
            # 更新读者当前借阅数量（减1）
            reader = record.reader
            reader.current_borrow_count -= 1
            reader.save()
            
            # 归还成功提示消息
            messages.success(request, '归还成功！')
            # 重定向到借阅记录列表页
            return redirect('borrow_list')
        except Exception as e:
            # 归还失败提示消息
            messages.error(request, f'归还失败：{str(e)}')
    
    # GET请求返回归还确认页面
    return render(request, 'borrows/borrow_return.html', {'record': record})