# 导入Django快捷函数：render用于渲染模板，redirect用于重定向，get_object_or_404用于获取对象或返回404
from django.shortcuts import render, redirect, get_object_or_404
# 导入Django消息框架，用于向用户显示提示信息
from django.contrib import messages
# 导入Book模型
from ..models import Book
# 导入分页器
from django.core.paginator import Paginator


def book_list(request):
    """
    图书列表视图函数
    :param request: HTTP请求对象
    :return: 渲染图书列表页面
    """
    # 获取所有图书对象
    books = Book.objects.all()
    # 创建分页器，每页显示10条记录
    paginator = Paginator(books, 10)
    # 获取当前页码（从URL参数中获取）
    page = request.GET.get('page')
    # 获取当前页的图书数据
    books_page = paginator.get_page(page)
    # 渲染模板并传递数据
    return render(request, 'books/book_list.html', {'books': books_page})


def book_detail(request, pk):
    """
    图书详情视图函数
    :param request: HTTP请求对象
    :param pk: 图书的主键ID
    :return: 渲染图书详情页面
    """
    # 根据主键获取图书对象，不存在则返回404
    book = get_object_or_404(Book, pk=pk)
    # 渲染模板并传递图书对象
    return render(request, 'books/book_detail.html', {'book': book})


def book_add(request):
    """
    添加图书视图函数
    :param request: HTTP请求对象
    :return: GET请求返回表单页面，POST请求处理表单提交
    """
    # 判断是否为POST请求（表单提交）
    if request.method == 'POST':
        try:
            # 创建Book对象并赋值
            book = Book(
                isbn=request.POST.get('isbn'),           # ISBN编号
                title=request.POST.get('title'),         # 书名
                author=request.POST.get('author'),       # 作者
                publisher=request.POST.get('publisher'), # 出版社
                publish_date=request.POST.get('publish_date'), # 出版日期
                category=request.POST.get('category'),   # 分类
                price=request.POST.get('price'),         # 价格
                total_quantity=request.POST.get('total_quantity', 0), # 总数量
                available_quantity=request.POST.get('available_quantity', 0), # 可借数量
                description=request.POST.get('description', '') # 简介
            )
            # 保存到数据库
            book.save()
            # 添加成功提示消息
            messages.success(request, '图书添加成功！')
            # 重定向到图书列表页
            return redirect('book_list')
        except Exception as e:
            # 添加失败提示消息
            messages.error(request, f'添加失败：{str(e)}')
    # GET请求返回表单页面
    return render(request, 'books/book_form.html')


def book_edit(request, pk):
    """
    编辑图书视图函数
    :param request: HTTP请求对象
    :param pk: 图书的主键ID
    :return: GET请求返回编辑表单页面，POST请求处理表单提交
    """
    # 根据主键获取图书对象，不存在则返回404
    book = get_object_or_404(Book, pk=pk)
    # 判断是否为POST请求（表单提交）
    if request.method == 'POST':
        try:
            # 更新图书对象的属性
            book.isbn = request.POST.get('isbn')
            book.title = request.POST.get('title')
            book.author = request.POST.get('author')
            book.publisher = request.POST.get('publisher')
            book.publish_date = request.POST.get('publish_date')
            book.category = request.POST.get('category')
            book.price = request.POST.get('price')
            book.total_quantity = request.POST.get('total_quantity', 0)
            book.available_quantity = request.POST.get('available_quantity', 0)
            book.description = request.POST.get('description', '')
            # 保存到数据库
            book.save()
            # 更新成功提示消息
            messages.success(request, '图书信息更新成功！')
            # 重定向到图书详情页
            return redirect('book_detail', pk=pk)
        except Exception as e:
            # 更新失败提示消息
            messages.error(request, f'更新失败：{str(e)}')
    # GET请求返回编辑表单页面，传递图书对象供表单显示
    return render(request, 'books/book_form.html', {'book': book})


def book_delete(request, pk):
    """
    删除图书视图函数
    :param request: HTTP请求对象
    :param pk: 图书的主键ID
    :return: GET请求返回确认删除页面，POST请求执行删除操作
    """
    # 根据主键获取图书对象，不存在则返回404
    book = get_object_or_404(Book, pk=pk)
    # 判断是否为POST请求（确认删除）
    if request.method == 'POST':
        # 删除图书对象
        book.delete()
        # 删除成功提示消息
        messages.success(request, '图书删除成功！')
        # 重定向到图书列表页
        return redirect('book_list')
    # GET请求返回确认删除页面
    return render(request, 'books/book_confirm_delete.html', {'book': book})