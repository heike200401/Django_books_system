# 导入Django数据库模型模块
from django.db import models
# 导入Django内置用户模型
from django.contrib.auth.models import User


class Book(models.Model):
    """
    图书模型类，用于存储图书信息
    """
    # 图书分类选项，元组格式：(数据库存储值, 显示名称)
    CATEGORY_CHOICES = [
        ('literature', '文学'),
        ('science', '科学'),
        ('technology', '技术'),
        ('history', '历史'),
        ('philosophy', '哲学'),
        ('art', '艺术'),
        ('other', '其他'),
    ]

    # ISBN编号，唯一标识，最大长度13位
    isbn = models.CharField(max_length=13, unique=True, verbose_name='ISBN')
    # 书名，最大长度200字符
    title = models.CharField(max_length=200, verbose_name='书名')
    # 作者，最大长度100字符
    author = models.CharField(max_length=100, verbose_name='作者')
    # 出版社，最大长度100字符
    publisher = models.CharField(max_length=100, verbose_name='出版社')
    # 出版日期
    publish_date = models.DateField(verbose_name='出版日期')
    # 分类，从预定义选项中选择
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='分类')
    # 价格，最大8位数字，2位小数
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='价格')
    # 总数量，默认为0
    total_quantity = models.IntegerField(default=0, verbose_name='总数量')
    # 可借数量，默认为0
    available_quantity = models.IntegerField(default=0, verbose_name='可借数量')
    # 简介，可选字段
    description = models.TextField(blank=True, verbose_name='简介')
    # 封面图片，上传到book_covers目录，可选字段
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True, verbose_name='封面')
    # 创建时间，自动记录创建时的时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间，自动记录每次更新的时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        # 在管理后台显示的单复数名称
        verbose_name = '图书'
        verbose_name_plural = '图书'
        # 默认按创建时间倒序排列
        ordering = ['-created_at']

    # 对象字符串表示，返回书名和作者
    def __str__(self):
        return f'{self.title} - {self.author}'


class Reader(models.Model):
    """
    读者模型类，用于存储读者信息
    """
    # 关联Django内置用户模型，一对一关系，删除用户时级联删除读者
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    # 联系电话，最大长度20字符
    phone = models.CharField(max_length=20, verbose_name='电话')
    # 地址，可选字段，最大长度200字符
    address = models.CharField(max_length=200, blank=True, verbose_name='地址')
    # 最大可借阅数量，默认5本
    max_borrow_count = models.IntegerField(default=5, verbose_name='最大借阅数')
    # 当前借阅数量，默认0本
    current_borrow_count = models.IntegerField(default=0, verbose_name='当前借阅数')
    # 注册时间，自动记录创建时的时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')

    class Meta:
        # 在管理后台显示的单复数名称
        verbose_name = '读者'
        verbose_name_plural = '读者'
        # 默认按注册时间倒序排列
        ordering = ['-created_at']

    # 对象字符串表示，返回用户名和真实姓名
    def __str__(self):
        return f'{self.user.username} - {self.user.first_name}{self.user.last_name}'


class BorrowRecord(models.Model):
    """
    借阅记录模型类，用于存储图书借阅信息
    """
    # 借阅状态选项
    STATUS_CHOICES = [
        ('borrowed', '借阅中'),
        ('returned', '已归还'),
        ('overdue', '已逾期'),
    ]

    # 关联图书模型，一对多关系，删除图书时级联删除借阅记录
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrow_records', verbose_name='图书')
    # 关联读者模型，一对多关系，删除读者时级联删除借阅记录
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name='borrow_records', verbose_name='读者')
    # 借阅日期，自动记录创建时的时间
    borrow_date = models.DateTimeField(auto_now_add=True, verbose_name='借阅日期')
    # 应还日期
    due_date = models.DateTimeField(verbose_name='应还日期')
    # 归还日期，可选字段，默认为空
    return_date = models.DateTimeField(null=True, blank=True, verbose_name='归还日期')
    # 借阅状态，从预定义选项中选择，默认为'借阅中'
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='borrowed', verbose_name='状态')
    # 罚金，最大6位数字，2位小数，默认为0
    fine = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='罚金')
    # 备注，可选字段
    notes = models.TextField(blank=True, verbose_name='备注')

    class Meta:
        # 在管理后台显示的单复数名称
        verbose_name = '借阅记录'
        verbose_name_plural = '借阅记录'
        # 默认按借阅日期倒序排列
        ordering = ['-borrow_date']

    # 对象字符串表示，返回读者用户名和图书标题
    def __str__(self):
        return f'{self.reader.user.username} - {self.book.title}'