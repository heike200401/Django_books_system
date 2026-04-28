# 导入Django快捷函数
from django.shortcuts import render, redirect, get_object_or_404
# 导入Django消息框架
from django.contrib import messages
# 导入Django内置用户模型
from django.contrib.auth.models import User
# 导入Reader模型
from ..models import Reader
# 导入分页器
from django.core.paginator import Paginator


def reader_list(request):
    """
    读者列表视图函数
    :param request: HTTP请求对象
    :return: 渲染读者列表页面
    """
    # 获取所有读者对象
    readers = Reader.objects.all()
    # 创建分页器，每页显示10条记录
    paginator = Paginator(readers, 10)
    # 获取当前页码
    page = request.GET.get('page')
    # 获取当前页的读者数据
    readers_page = paginator.get_page(page)
    # 渲染模板并传递数据
    return render(request, 'readers/reader_list.html', {'readers': readers_page})


def reader_detail(request, pk):
    """
    读者详情视图函数
    :param request: HTTP请求对象
    :param pk: 读者的主键ID
    :return: 渲染读者详情页面
    """
    # 根据主键获取读者对象，不存在则返回404
    reader = get_object_or_404(Reader, pk=pk)
    # 渲染模板并传递读者对象
    return render(request, 'readers/reader_detail.html', {'reader': reader})


def reader_add(request):
    """
    添加读者视图函数
    :param request: HTTP请求对象
    :return: GET请求返回表单页面，POST请求处理表单提交
    """
    # 判断是否为POST请求（表单提交）
    if request.method == 'POST':
        try:
            # 获取表单数据
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            # 创建Django用户对象
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            
            # 创建Reader对象并关联用户
            reader = Reader(
                user=user,
                phone=request.POST.get('phone'),
                address=request.POST.get('address', ''),
                max_borrow_count=request.POST.get('max_borrow_count', 5)
            )
            # 保存到数据库
            reader.save()
            # 添加成功提示消息
            messages.success(request, '读者添加成功！')
            # 重定向到读者列表页
            return redirect('reader_list')
        except Exception as e:
            # 添加失败提示消息
            messages.error(request, f'添加失败：{str(e)}')
    # GET请求返回表单页面
    return render(request, 'readers/reader_form.html')


def reader_edit(request, pk):
    """
    编辑读者视图函数
    :param request: HTTP请求对象
    :param pk: 读者的主键ID
    :return: GET请求返回编辑表单页面，POST请求处理表单提交
    """
    # 根据主键获取读者对象，不存在则返回404
    reader = get_object_or_404(Reader, pk=pk)
    # 判断是否为POST请求（表单提交）
    if request.method == 'POST':
        try:
            # 更新关联的用户对象信息
            reader.user.first_name = request.POST.get('first_name')
            reader.user.last_name = request.POST.get('last_name')
            reader.user.email = request.POST.get('email')
            reader.user.save()
            
            # 更新读者对象信息
            reader.phone = request.POST.get('phone')
            reader.address = request.POST.get('address', '')
            reader.max_borrow_count = request.POST.get('max_borrow_count', 5)
            reader.save()
            # 更新成功提示消息
            messages.success(request, '读者信息更新成功！')
            # 重定向到读者详情页
            return redirect('reader_detail', pk=pk)
        except Exception as e:
            # 更新失败提示消息
            messages.error(request, f'更新失败：{str(e)}')
    # GET请求返回编辑表单页面，传递读者对象供表单显示
    return render(request, 'readers/reader_form.html', {'reader': reader})


def reader_delete(request, pk):
    """
    删除读者视图函数
    :param request: HTTP请求对象
    :param pk: 读者的主键ID
    :return: GET请求返回确认删除页面，POST请求执行删除操作
    """
    # 根据主键获取读者对象，不存在则返回404
    reader = get_object_or_404(Reader, pk=pk)
    # 判断是否为POST请求（确认删除）
    if request.method == 'POST':
        # 保存关联的用户对象引用（因为删除读者后用户对象也需要删除）
        user = reader.user
        # 删除读者对象
        reader.delete()
        # 删除关联的用户对象
        user.delete()
        # 删除成功提示消息
        messages.success(request, '读者删除成功！')
        # 重定向到读者列表页
        return redirect('reader_list')
    # GET请求返回确认删除页面
    return render(request, 'readers/reader_confirm_delete.html', {'reader': reader})