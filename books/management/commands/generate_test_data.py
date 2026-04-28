import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from books.models import Book, Reader, BorrowRecord


class Command(BaseCommand):
    help = '生成测试数据'

    def handle(self, *args, **kwargs):
        self.stdout.write('正在生成测试数据...')

        # 图书数据
        books_data = [
            {'isbn': '9787115428028', 'title': 'Python编程：从入门到实践', 'author': 'Eric Matthes', 'publisher': '人民邮电出版社', 'publish_date': '2016-07-01', 'category': 'technology', 'price': 89.00, 'total_quantity': 10, 'available_quantity': 8, 'description': '一本非常好的Python入门书籍，适合初学者阅读。'},
            {'isbn': '9787111544937', 'title': '深入理解计算机系统', 'author': 'Randal E. Bryant', 'publisher': '机械工业出版社', 'publish_date': '2016-11-01', 'category': 'science', 'price': 139.00, 'total_quantity': 5, 'available_quantity': 3, 'description': '计算机科学经典教材，深入讲解计算机系统原理。'},
            {'isbn': '9787115279460', 'title': '算法导论', 'author': 'Thomas H. Cormen', 'publisher': '机械工业出版社', 'publish_date': '2013-01-01', 'category': 'technology', 'price': 128.00, 'total_quantity': 8, 'available_quantity': 6, 'description': '算法领域的经典教材，全面介绍各种算法和数据结构。'},
            {'isbn': '9787020002207', 'title': '红楼梦', 'author': '曹雪芹', 'publisher': '人民文学出版社', 'publish_date': '1996-12-01', 'category': 'literature', 'price': 59.70, 'total_quantity': 15, 'available_quantity': 12, 'description': '中国古典四大名著之一，讲述贾宝玉与林黛玉的爱情故事。'},
            {'isbn': '9787020002208', 'title': '三国演义', 'author': '罗贯中', 'publisher': '人民文学出版社', 'publish_date': '1996-12-01', 'category': 'literature', 'price': 49.80, 'total_quantity': 12, 'available_quantity': 10, 'description': '中国古典四大名著之一，描写三国时期的政治军事斗争。'},
            {'isbn': '9787111213826', 'title': '设计模式：可复用面向对象软件的基础', 'author': 'Erich Gamma', 'publisher': '机械工业出版社', 'publish_date': '2007-11-01', 'category': 'technology', 'price': 55.00, 'total_quantity': 7, 'available_quantity': 5, 'description': '软件设计模式的经典著作，介绍23种常用设计模式。'},
            {'isbn': '9787115418996', 'title': 'JavaScript高级程序设计', 'author': 'Nicholas C. Zakas', 'publisher': '人民邮电出版社', 'publish_date': '2012-03-01', 'category': 'technology', 'price': 99.00, 'total_quantity': 9, 'available_quantity': 7, 'description': 'JavaScript学习的经典教材，全面讲解JavaScript语言特性。'},
            {'isbn': '9787100001454', 'title': '史记', 'author': '司马迁', 'publisher': '中华书局', 'publish_date': '2013-01-01', 'category': 'history', 'price': 198.00, 'total_quantity': 6, 'available_quantity': 4, 'description': '中国第一部纪传体通史，记载了从黄帝到汉武帝的历史。'},
            {'isbn': '9787108012636', 'title': '万历十五年', 'author': '黄仁宇', 'publisher': '生活·读书·新知三联书店', 'publish_date': '2014-09-01', 'category': 'history', 'price': 39.00, 'total_quantity': 11, 'available_quantity': 9, 'description': '以小见大，通过万历十五年的细节展现明代社会风貌。'},
            {'isbn': '9787100023746', 'title': '中国哲学史', 'author': '冯友兰', 'publisher': '商务印书馆', 'publish_date': '2011-09-01', 'category': 'philosophy', 'price': 78.00, 'total_quantity': 5, 'available_quantity': 3, 'description': '冯友兰先生的代表作，系统介绍中国哲学发展历史。'},
            {'isbn': '9787532753538', 'title': '百年孤独', 'author': '加西亚·马尔克斯', 'publisher': '上海译文出版社', 'publish_date': '2011-06-01', 'category': 'literature', 'price': 39.50, 'total_quantity': 13, 'available_quantity': 11, 'description': '魔幻现实主义文学的代表作，讲述布恩迪亚家族七代人的故事。'},
            {'isbn': '9787115358150', 'title': '代码整洁之道', 'author': 'Robert C. Martin', 'publisher': '人民邮电出版社', 'publish_date': '2010-01-01', 'category': 'technology', 'price': 59.00, 'total_quantity': 8, 'available_quantity': 6, 'description': '讲解如何编写整洁、可维护的代码，提升代码质量。'},
            {'isbn': '9787111587542', 'title': '重构：改善既有代码的设计', 'author': 'Martin Fowler', 'publisher': '机械工业出版社', 'publish_date': '2019-03-01', 'category': 'technology', 'price': 89.00, 'total_quantity': 6, 'available_quantity': 4, 'description': '讲解代码重构的技巧和最佳实践，帮助改善代码质量。'},
            {'isbn': '9787115485509', 'title': '人类简史', 'author': '尤瓦尔·赫拉利', 'publisher': '中信出版社', 'publish_date': '2017-02-01', 'category': 'history', 'price': 68.00, 'total_quantity': 10, 'available_quantity': 8, 'description': '从认知革命到科学革命，讲述人类进化的历史。'},
            {'isbn': '9787111607882', 'title': '未来简史', 'author': '尤瓦尔·赫拉利', 'publisher': '中信出版社', 'publish_date': '2017-03-01', 'category': 'science', 'price': 68.00, 'total_quantity': 8, 'available_quantity': 6, 'description': '探讨人工智能时代人类的未来和命运。'},
            {'isbn': '9787108008989', 'title': '美的历程', 'author': '李泽厚', 'publisher': '生活·读书·新知三联书店', 'publish_date': '2009-07-01', 'category': 'art', 'price': 36.00, 'total_quantity': 7, 'available_quantity': 5, 'description': '李泽厚的美学著作，讲述中国艺术的发展历程。'},
            {'isbn': '9787506336274', 'title': '艺术的故事', 'author': '贡布里希', 'publisher': '广西美术出版社', 'publish_date': '2015-06-01', 'category': 'art', 'price': 280.00, 'total_quantity': 4, 'available_quantity': 3, 'description': '艺术史的经典著作，图文并茂地介绍艺术发展史。'},
            {'isbn': '9787100078061', 'title': '存在与时间', 'author': '海德格尔', 'publisher': '生活·读书·新知三联书店', 'publish_date': '2014-09-01', 'category': 'philosophy', 'price': 68.00, 'total_quantity': 3, 'available_quantity': 2, 'description': '海德格尔的代表作，探讨存在的意义问题。'},
            {'isbn': '9787115423429', 'title': '机器学习', 'author': '周志华', 'publisher': '清华大学出版社', 'publish_date': '2016-01-01', 'category': 'science', 'price': 88.00, 'total_quantity': 9, 'available_quantity': 7, 'description': '机器学习领域的中文经典教材，全面介绍机器学习算法。'},
            {'isbn': '9787111396455', 'title': '统计学习方法', 'author': '李航', 'publisher': '清华大学出版社', 'publish_date': '2012-03-01', 'category': 'science', 'price': 68.00, 'total_quantity': 8, 'available_quantity': 6, 'description': '统计学习方法的经典教材，介绍常用的统计学习算法。'},
        ]

        # 创建图书
        books = []
        for data in books_data:
            book, created = Book.objects.get_or_create(
                isbn=data['isbn'],
                defaults=data
            )
            books.append(book)
            if created:
                self.stdout.write(f'创建图书: {book.title}')

        # 读者数据
        readers_data = [
            {'username': 'zhangsan', 'first_name': '三', 'last_name': '张', 'email': 'zhangsan@example.com', 'password': '123456', 'phone': '13800138001', 'address': '北京市海淀区', 'max_borrow_count': 5},
            {'username': 'lisi', 'first_name': '四', 'last_name': '李', 'email': 'lisi@example.com', 'password': '123456', 'phone': '13800138002', 'address': '上海市浦东新区', 'max_borrow_count': 5},
            {'username': 'wangwu', 'first_name': '五', 'last_name': '王', 'email': 'wangwu@example.com', 'password': '123456', 'phone': '13800138003', 'address': '广州市天河区', 'max_borrow_count': 8},
            {'username': 'zhaoliu', 'first_name': '六', 'last_name': '赵', 'email': 'zhaoliu@example.com', 'password': '123456', 'phone': '13800138004', 'address': '深圳市南山区', 'max_borrow_count': 5},
            {'username': 'sunqi', 'first_name': '七', 'last_name': '孙', 'email': 'sunqi@example.com', 'password': '123456', 'phone': '13800138005', 'address': '杭州市西湖区', 'max_borrow_count': 10},
        ]

        # 创建读者
        readers = []
        for data in readers_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'email': data['email']
                }
            )
            if created:
                user.set_password(data['password'])
                user.save()

            reader, created = Reader.objects.get_or_create(
                user=user,
                defaults={
                    'phone': data['phone'],
                    'address': data['address'],
                    'max_borrow_count': data['max_borrow_count']
                }
            )
            readers.append(reader)
            if created:
                self.stdout.write(f'创建读者: {reader.user.username}')

        # 创建借阅记录
        borrow_records_data = [
            {'book': books[0], 'reader': readers[0], 'days_ago': 15, 'days_duration': 30, 'returned': True},
            {'book': books[1], 'reader': readers[0], 'days_ago': 10, 'days_duration': 30, 'returned': False},
            {'book': books[3], 'reader': readers[1], 'days_ago': 20, 'days_duration': 30, 'returned': True},
            {'book': books[4], 'reader': readers[1], 'days_ago': 5, 'days_duration': 30, 'returned': False},
            {'book': books[6], 'reader': readers[2], 'days_ago': 25, 'days_duration': 30, 'returned': False},
            {'book': books[8], 'reader': readers[2], 'days_ago': 8, 'days_duration': 30, 'returned': False},
            {'book': books[10], 'reader': readers[2], 'days_ago': 35, 'days_duration': 30, 'returned': True, 'overdue': True},
            {'book': books[12], 'reader': readers[3], 'days_ago': 12, 'days_duration': 60, 'returned': False},
            {'book': books[14], 'reader': readers[3], 'days_ago': 3, 'days_duration': 30, 'returned': False},
            {'book': books[16], 'reader': readers[4], 'days_ago': 40, 'days_duration': 30, 'returned': True, 'overdue': True},
        ]

        for data in borrow_records_data:
            borrow_date = datetime.now() - timedelta(days=data['days_ago'])
            due_date = borrow_date + timedelta(days=data['days_duration'])
            
            borrow_record = BorrowRecord.objects.create(
                book=data['book'],
                reader=data['reader'],
                due_date=due_date,
                status='borrowed'
            )
            borrow_record.borrow_date = borrow_date
            borrow_record.save()

            if data['returned']:
                borrow_record.return_date = borrow_date + timedelta(days=data['days_ago'] - 2)
                borrow_record.status = 'returned'
                if data.get('overdue', False):
                    borrow_record.status = 'overdue'
                    borrow_record.fine = (borrow_record.return_date - borrow_record.due_date).days * 0.5
                borrow_record.save()

            self.stdout.write(f'创建借阅记录: {borrow_record}')

        self.stdout.write(self.style.SUCCESS('测试数据生成完成！'))
