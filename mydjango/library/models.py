from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.db.models import Max

def get_default_start_time():
    return timezone.now()

def get_default_ddl():
    return timezone.now() + timedelta(days=30)

class Author(models.Model):
    authorID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    introduction = models.TextField(null=True)

    def __str__(self):
        return self.name
    
    @classmethod
    def generate_author_id(cls):
        # 获取当前作者ID的最大值
        max_id = cls.objects.aggregate(Max('authorID'))['authorID__max']
        return str(int(max_id) + 1) if max_id is not None else '1'

class Bookshelf(models.Model):
    bookID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    amount = models.IntegerField()
    lend_amount = models.IntegerField()  # 修改这个字段名称
    introduction = models.TextField(null=True)

    def __str__(self):
        return self.title
    
    @classmethod
    def generate_book_id(cls):
        max_id = cls.objects.aggregate(Max('bookID'))['bookID__max']
        return str(int(max_id) + 1) if max_id is not None else '1'

class Administrator(models.Model):
    adminID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    account = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    @classmethod
    def check_password(cls, account, password):
        try:
            user = cls.objects.get(account=account)
            if user.password == password:
                # 返回该用户的所有信息
                return user
            else:
                return None
        except:
            return None
    
    @classmethod
    def generate_admin_id(cls):
        max_id = cls.objects.aggregate(Max('adminID'))['adminID__max']
        return str(int(max_id) + 1) if max_id is not None else '1'

class User(models.Model):
    userID = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=255)
    phoneNum = models.CharField(max_length=20)
    account = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    borrowTimes = models.IntegerField()
    ovdTimes = models.IntegerField()

    def __str__(self):
        return self.name
    
    @classmethod
    def generate_user_id(cls):
         # 获取当前用户ID的最大值
        max_id = cls.objects.aggregate(Max('userID'))['userID__max']
        return str(int(max_id) + 1) if max_id is not None else '1'
    
    @classmethod
    def check_password(cls, account, password):
        try:
            user = cls.objects.get(account=account)
            if user.password == password:
                # 返回该用户的所有信息
                return user
            else:
                return None
        except:
            return None

class Lend(models.Model):
    lendID = models.AutoField(primary_key=True)
    reserveID = models.IntegerField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Bookshelf, on_delete=models.CASCADE)
    startTime = models.DateTimeField(default=get_default_start_time)
    DDL = models.DateTimeField(default=get_default_ddl)  # 设置为30天后
    endTime = models.DateTimeField(null=True)

    def __str__(self):
        return f"Lend {self.lendID} - {self.book.title}"
    
    @classmethod
    def generate_lend_id(cls):
        max_id = cls.objects.aggregate(Max('lendID'))['lendID__max']
        return str(int(max_id) + 1) if max_id is not None else '1'
    
    @classmethod
    def set_end_time(cls, lendID):
        lend = cls.objects.get(lendID=lendID)
        lend.endTime = timezone.now()
        lend.save()
    
class Reserve(models.Model):
    reserveID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    bookID = models.ForeignKey(Bookshelf, on_delete=models.CASCADE)
    startTime = models.DateTimeField(default=get_default_start_time)  # 设置为当前时间
    DDL = models.DateTimeField(default=get_default_ddl)  # 设置为30天后
    endTime = models.DateTimeField(null=True)

    @classmethod
    def is_reserved(cls, userID, bookID):
        return cls.objects.filter(bookID=bookID, userID=userID).exists()
        
    @classmethod
    def generate_reserve_id(cls):
        max_id = cls.objects.aggregate(Max('reserveID'))['reserveID__max']
        return str(int(max_id) + 1) if max_id is not None else '1'
    
    @classmethod
    def set_end_time(cls, reserveID):
        reserve = cls.objects.get(reserveID=reserveID)
        reserve.endTime = timezone.now()
        reserve.save()

class Quotation(models.Model):
    quotationID = models.AutoField(primary_key=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    quotation = models.TextField()

    def __str__(self):
        return f"Quotation {self.quotationID} - {self.author.name}"
    
    @classmethod
    def generate_quotation_id(cls):
        max_id = cls.objects.aggregate(Max('quotationID'))['quotationID__max']
        return str(int(max_id) + 1) if max_id is not None else '1'

class Backgroud(models.Model):
    backgroundID = models.AutoField(primary_key=True)
    url = models.CharField(max_length=255)

class Message(models.Model):
    messageID = models.AutoField(primary_key=True)
    sender = models.ForeignKey(Administrator, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(default=get_default_start_time)
    isRead = models.BooleanField(default=False)

    def __str__(self):
        return f"Message {self.messageID} - {self.sender.name} -> {self.receiver.name}"
    
    @classmethod
    def generate_message_id(cls):
        max_id = cls.objects.aggregate(Max('messageID'))['messageID__max']
        return str(int(max_id) + 1) if max_id is not None else '1'
    

