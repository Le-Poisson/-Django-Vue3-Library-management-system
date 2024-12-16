from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Administrator, Reserve, Bookshelf, Author, Lend, Quotation, Message  # 确保导入自定义用户模型
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.db.models import Q
from pypinyin import pinyin, Style
from datetime import datetime, timedelta
from django.utils import timezone
from django.db import transaction

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the library index.")

# users/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import status

@api_view(['POST'])
def handle_post(request):
    print(request.data)
    print(request.headers.get('X-Requested-With'))
    label = request.headers.get('X-Requested-With')
    # 从 headers 中获取标识
    if label == 'Registration':
        return register(request)
    elif label == 'Login':
        return login(request)
    elif label == 'Admin_Login':
        return admin_login(request)
    elif label == 'Search':
        return search(request)
    elif label == 'Get_All_Books':
        return get_all_books(request)
    elif label == 'Get_All_Users':
        return get_all_users(request)
    elif label == 'Delete_User':
        return delete_user(request)
    elif label == 'Delete_Book':
        return delete_book(request)
    elif label == 'Book_Reserve':
        return book_reserve(request)
    elif label == 'Search_Reserve':
        return search_reserve(request)
    elif label == 'Get_All_Reserves':
        return get_all_reserves(request)
    elif label == 'Add_Book':
        return add_book(request)
    elif label == 'Add_Author':
        return add_author(request)
    elif label == 'Change_Book_Info':
        return change_book_info(request)
    elif label == 'Return_Book':
        return return_book(request)
    elif label == 'Get_Borrows':
        return get_borrows(request)
    elif label == 'Continue_Borrow_Book':
        return continue_borrow_book(request)
    elif label == 'AddQuotations':
        return add_quotations(request)
    elif label == 'Get_Quotations':
        return get_quotations(request)
    elif label == 'Delete_Quotation':
        return delete_quotation(request)
    elif label == 'Search_Quotations':
        return search_quotations(request)
    elif label == 'Edit_Quotation':
        return edit_quotation(request)
    elif label == 'Send_Message':
        return send_message(request)
    elif label == 'Get_Messages':
        return get_messages(request)
    elif label == 'Delete_Message':
        return delete_message(request)
    
    
    
    
    print("请求类型错误")
    return Response({'success': False, 'message': '请求类型错误'}, status=status.HTTP_400_BAD_REQUEST)

def register(request):
    user_id = User.generate_user_id()  # 生成新的 userID
    name = request.data.get('fullName')
    phone_num = request.data.get('phone')
    account = request.data.get('username')  # 确保从请求中获取账户名
    password = request.data.get('password')
    print("用户注册，用户信息为：", user_id, name, phone_num, account, password)

    # 检查是否缺少必要字段
    if not all([user_id, name, phone_num, account, password]):
        return Response({'success': False, 'message': '缺少必要字段'})

    if User.objects.filter(account=account).exists():
        print("该账号已被注册")
        return Response({'success': False, 'message': '该账号已被注册'})

    # 创建用户
    user = User(
        userID=user_id,
        name=name,
        phoneNum=phone_num,
        account=account,
        password=password,  # 使用哈希存储密码
        borrowTimes = 0,
        ovdTimes = 0
    )
    user.save()  # 保存用户
    print("用户注册成功")

    return Response({
        'success': True,
        'user': {
            'userID': user.userID,
            'name': user.name,
            'phoneNum': user.phoneNum,
            'account': user.account,
            'borrowTimes' : user.borrowTimes,
            'ovdTimes' : user.ovdTimes
        }
    }, status=status.HTTP_201_CREATED)  # 返回成功响应

def login(request):
    account = request.data.get('username')  # 从请求中获取用户名
    password = request.data.get('password')  # 从请求中获取密码
    print("用户登录，账号密码为：",account, password)

    # 检查是否提供了用户名和密码
    if not all([account, password]):
        return Response({'success': False, 'message': '缺少用户名或密码'}, status=status.HTTP_400_BAD_REQUEST)

    # 认证用户
    user = User.check_password(account, password)

    if user is not None:
        # 用户认证成功
        return Response({
            'success': True,
            'user': {
                'userID': user.userID,
                'name': user.name,
                'phoneNum': user.phoneNum,
                'account': user.account,
                'borrowTimes' : user.borrowTimes,
                'ovdTimes' : user.ovdTimes
            }
        }, status=status.HTTP_200_OK)
    else:
        print("用户名或密码错误")
        # 用户认证失败
        return Response({'success': False, 'message': '用户名或密码错误'})

def admin_login(request):
    username = request.data.get('username')  # 从请求中获取用户名
    password = request.data.get('password')  # 从请求中获取密码
    print("管理员登录，账号密码为：",username, password)

    # 检查是否提供了用户名和密码
    if not all([username, password]):
        return Response({'success': False, 'message': '缺少用户名或密码'}, status=status.HTTP_400_BAD_REQUEST)

    user = Administrator.check_password(username, password)

    if user is not None:
        # 管理员认证成功
        return Response({
            'success': True,
            'admin': {
                'adminID': user.adminID,
                'name': user.name,
                'account': user.account,
            }
        }, status=status.HTTP_200_OK)
    else:
        print("用户名或密码错误")
        # 管理员认证失败
        return Response({'success': False, 'message': '用户名或密码错误'})


def search(request):
    book_name = request.data.get('bookName')  # 获取请求中的书名
    print("用户搜索，书名为：", book_name)

    if book_name:
        # 查询符合条件的书籍
        # books = Bookshelf.objects.filter(title__icontains=book_name)
        books = Bookshelf.objects.filter(
            Q(title__icontains=book_name) | Q(author__name__icontains=book_name)
        )
        # 将查询结果转换为字典列表
        books_list = list(books.values('bookID', 'title', 'author__name', 'amount', 'lend_amount'))
        
        # 按拼音排序
        books_list.sort(key=lambda x: ''.join([item for sublist in pinyin(x['title'], style=Style.NORMAL) for item in sublist]))

        print("查询结果：", books_list)
        # 返回成功响应
        return Response({'success': True, 'books': books_list})
    else:
        # 返回失败响应，未提供书名
        # return Response({'success': False, 'message': '书名不能为空'})
        books = Bookshelf.objects.all()
        books_list = list(books.values('bookID', 'title', 'author__name', 'amount', 'lend_amount', 'introduction'))
        # 按拼音排序
        books_list.sort(key=lambda x: ''.join([item for sublist in pinyin(x['title'], style=Style.NORMAL) for item in sublist]))
        
        print("所有书籍：", books_list)
        # 返回成功响应
        return Response({'success': True, 'books': books_list})
    
def get_all_books(request):
    books = Bookshelf.objects.all()
    books_list = list(books.values('bookID', 'title', 'author__name', 'amount', 'lend_amount', 'introduction'))
    # 按拼音排序
    books_list.sort(key=lambda x: ''.join([item for sublist in pinyin(x['title'], style=Style.NORMAL) for item in sublist]))
    
    print("所有书籍：", books_list)
    # 返回成功响应
    return Response({'success': True, 'books': books_list})

def get_all_users(request):
    users = User.objects.all()
    usersList = list(users.values('userID', 'name', 'phoneNum', 'account', 'borrowTimes', 'ovdTimes'))
    # 按拼音排序
    usersList.sort(key=lambda x: ''.join([item for sublist in pinyin(x['name'], style=Style.NORMAL) for item in sublist]))
    
    print("所有用户：", usersList)
    # 返回成功响应
    return Response({'success': True, 'userList': usersList})

def delete_user(request):
    userID = request.data.get('userID')  # 获取请求中的用户ID
    print("删除用户，用户ID为：", userID)

    if userID:
        user = User.objects.get(userID=userID)
        borrows = Reserve.objects.filter(userID=user)
        borrows_list = list(borrows.values('reserveID', 'bookID__bookID', 'userID__name', 'startTime', 'DDL'))
        for borrow in borrows_list:
            book = Bookshelf.objects.get(bookID=borrow['bookID__bookID'])
            book.lend_amount -= 1
            book.save()
            print("还书：", book.title, "，还书人：", user.name)
        # 删除用户
        User.objects.filter(userID=userID).delete()

        users = User.objects.all()
        usersList = list(users.values('userID', 'name', 'phoneNum', 'account', 'borrowTimes', 'ovdTimes'))
        # 按拼音排序
        usersList.sort(key=lambda x: ''.join([item for sublist in pinyin(x['name'], style=Style.NORMAL) for item in sublist]))
    
        print("所有用户：", usersList)
        # 返回成功响应
        return Response({'success': True, 'userList': usersList})
    else:
        # 返回失败响应，未提供用户ID
        return Response({'success': False, 'message': '用户ID不能为空'})
    
def delete_book(request):
    bookID = request.data.get('bookID')  # 获取请求中的书ID
    print("删除书籍，书ID为：", bookID)

    if bookID:
        # 删除书籍
        Bookshelf.objects.filter(bookID=bookID).delete()

        books = Bookshelf.objects.all()
        books_list = list(books.values('bookID', 'title', 'author__name', 'amount', 'lend_amount'))
        # 按拼音排序
        books_list.sort(key=lambda x: ''.join([item for sublist in pinyin(x['title'], style=Style.NORMAL) for item in sublist]))

        print("所有书籍：", books_list)
        # 返回成功响应
        return Response({'success': True, 'books': books_list})
    else:
        # 返回失败响应，未提供书ID
        return Response({'success': False, 'message': '书ID不能为空'})

def book_reserve(request):
    bookID = request.data.get('bookID')  # 获取请求中的书ID
    userID = request.data.get('userID')  # 获取请求中的用户ID
    print("借阅书籍，书ID为：", bookID, "，用户ID为：", userID)

    if bookID and userID:
        # 查询书籍
        book = Bookshelf.objects.get(bookID=bookID)
        # 查询用户
        user = User.objects.get(userID=userID)

        if Reserve.is_reserved(user, book):
            # 该用户已预定过该书籍
            return Response({'success': False, 'message': '请勿重复借阅'})

        if book.lend_amount >= book.amount:
            # 书籍已借完
            return Response({'success': False, 'message': '该书籍已借完'})
        
        lend = Lend(
            lendID=Lend.generate_lend_id(),
            reserveID=Reserve.generate_reserve_id(),
            book=book,
            user=user,
        )
        lend.save()  # 保存借阅信息

        reserve = Reserve(
            reserveID=Reserve.generate_reserve_id(),
            bookID=book,
            userID=user,
        )
        reserve.save()  # 保存预定信息

        # 借阅书籍
        book.lend_amount += 1
        user.borrowTimes += 1
        # 保存数据
        book.save()
        user.save()
        # 返回成功响应
        return Response({'success': True})
    else:
        # 返回失败响应，未提供书ID或用户ID
        return Response({'success': False, 'message': '书ID或用户ID不能为空'})

def search_reserve(request):
    info = request.data.get('info')  # 获取请求中的预定ID
    print("查询预定信息：", info)

    # 分别在用户名和书名中搜索
    if info:
        # 查询符合条件的预定信息
        reserves = Reserve.objects.filter(
            Q(userID__name__icontains=info) | Q(bookID__title__icontains=info)
        )
        # 将查询结果转换为字典列表
        reserves_list = list(reserves.values('reserveID', 'bookID__title', 'userID__name', 'startTime', 'DDL', 'endTime'))
        print("查询结果：", reserves_list)
        # 返回成功响应
        return Response({'success': True,'reserves': reserves_list})
    else:
        # 返回所有用户信息
        reserves = Reserve.objects.all()
        reserves_list = list(reserves.values('reserveID', 'bookID__title', 'userID__name', 'startTime', 'DDL', 'endTime'))
        print("所有预定信息：", reserves_list)
        # 返回成功响应
        return Response({'success': True,'reserves': reserves_list})

def get_all_reserves(request):
    reserves = Reserve.objects.all()
    reserves_list = list(reserves.values('reserveID', 'bookID__title', 'userID__name', 'startTime', 'DDL', 'endTime'))
    print("所有预定信息：", reserves_list)
    # 返回成功响应
    return Response({'success': True,'reserves': reserves_list})

def add_book(request):
    title = request.data.get('title')  # 获取请求中的书名
    author = request.data.get('author')  # 获取请求中的作者名
    amount = request.data.get('amount')  # 获取请求中的数量
    introduction = request.data.get('introduce')  # 获取请求中的介绍
    print("添加书籍，书名为：", title, "，作者为：", author, "，数量为：", amount, "，介绍为：", introduction)

    if title and author and amount:
        # 先判断是否存在该书籍
        if Bookshelf.objects.filter(title=title).exists():
            # 该书籍已存在
            return Response({'success': False, 'message': '该书籍已存在'})
        
        # 再判断作者是否存在
        if not Author.objects.filter(name=author).exists():
            # 作者不存在，创建作者
            author = Author(
                authorID=Author.generate_author_id(),
                name=author,
            )
            author.save()  # 保存作者

        # 提取出作者
        author = Author.objects.get(name=author)

        # 创建书籍
        book = Bookshelf(
            bookID=Bookshelf.generate_book_id(),
            title=title,
            author=author,
            amount=amount,
            introduction=introduction,
            lend_amount=0
        )
        book.save()  # 保存书籍
        print("书籍添加成功")
        # 返回成功响应
        return Response({'success': True})
    else:
        # 返回失败响应，缺少必要字段
        return Response({'success': False, 'message': '缺少必要字段'})
    
def add_author(request):
    name = request.data.get('name')  # 获取请求中的作者名
    introction = request.data.get('introduction')  # 获取请求中的介绍
    print("添加作者，作者名为：", name, "，介绍为：", introction)

    if name:
        # 先判断是否存在该作者
        if Author.objects.filter(name=name).exists():
            # 该作者已存在
            return Response({'success': False, 'message': '该作者已存在'})

        # 创建作者
        author = Author(
            authorID=Author.generate_author_id(),
            name=name,
            introduction=introction
        )
        author.save()  # 保存作者
        print("作者添加成功")
        # 返回成功响应
        return Response({'success': True})
    else:
        # 返回失败响应，缺少必要字段
        return Response({'success': False, 'message': '缺少必要字段'})
    
def change_book_info(request):
    bookID = request.data.get('bookID')  # 获取请求中的书ID
    title = request.data.get('bookName')  # 获取请求中的新书名
    author = request.data.get('bookAuthor')  # 获取请求中的新作者名
    amount = request.data.get('bookAmount')  # 获取请求中的新数量
    introduction = request.data.get('bookIntroduction')  # 获取请求中的新介绍
    print("修改书籍信息，书ID为：", bookID, "，书名为：", title, "，数量为：", amount, "，介绍为：", introduction)
    
    # 查询书籍
    book = Bookshelf.objects.get(bookID=bookID)
    if book:
        # 查找作者是否存在
        if not Author.objects.filter(name=author).exists():
            # 作者不存在，更改失败
            return Response({'success': False, 'message': '作者不存在'})
        # 修改书籍信息
        book.title = title
        book.author = Author.objects.get(name=author)
        book.amount = amount
        book.introduction = introduction
        
        book.save()  # 保存书籍

        # 返回成功响应
        books = Bookshelf.objects.all()
        books_list = list(books.values('bookID', 'title', 'author__name', 'amount', 'lend_amount'))
        # 按拼音排序
        books_list.sort(key=lambda x: ''.join([item for sublist in pinyin(x['title'], style=Style.NORMAL) for item in sublist]))

        print("所有书籍：", books_list)
        # 返回成功响应
        return Response({'success': True, 'books': books_list})
    else:
        # 返回失败响应，未找到书籍
        return Response({'success': False, 'message': '未找到书籍'})

def return_book(request):
    reserveID = request.data.get('reserveID')  # 获取请求中的预定ID
    print("归还书籍，预定ID为：", reserveID)

    # 查询预定信息
    reserve = Reserve.objects.get(reserveID=reserveID)
    lend = Lend.objects.get(reserveID=reserveID)
    if reserve:
        # 归还书籍
        book = reserve.bookID
        book.lend_amount -= 1
        # 保存数据
        book.save()
        # 删除预定信息
        reserve.delete()
        # 返回成功响应
        Lend.set_end_time(lend.lendID)

        return Response({'success': True})
    else:
        # 返回失败响应，未找到预定信息
        return Response({'success': False, 'message': '未找到预定信息'})

def continue_borrow_book(request):
    reserveID = request.data.get('reserveID')  # 从请求中获取预定 ID
    print("续借书籍，预定 ID 为：", reserveID)

    # 查询预定信息和对应的借阅记录
    try:
        with transaction.atomic():  # 确保操作是原子的
            reserve = Reserve.objects.get(reserveID=reserveID)
            lend = Lend.objects.filter(reserveID=reserveID, endTime__isnull=True).first()

            if lend is None:
                return Response({'success': False, 'message': '未找到合适的借阅记录'})

            # 更新用户借书次数
            user = reserve.userID
            user.borrowTimes += 1
            user.save()

            # 设置当前借阅的结束时间
            lend.endTime = timezone.now()
            lend.save()

            # 创建新的预定信息
            new_reserve = Reserve(
                reserveID=Reserve.generate_reserve_id(),
                bookID=reserve.bookID,
                userID=user,
            )
            new_reserve.save()  # 自动生成 reserveID

            # 创建新的借阅记录
            new_lend = Lend(
                lendID=Lend.generate_lend_id(),
                reserveID=new_reserve.reserveID,
                book=reserve.bookID,
                user=user,
            )
            new_lend.save()  # 自动生成 lendID

            # 删除旧的预定信息
            reserve.delete()

            # 返回成功响应，包含新的预定 ID
            return Response({'success': True, 'new_reserveID': new_reserve.reserveID})

    except Reserve.DoesNotExist:
        return Response({'success': False, 'message': '未找到预定信息'})
    except Exception as e:
        return Response({'success': False, 'message': str(e)})

def get_borrows(request):
    userID = request.data.get('userID')  # 获取请求中的用户ID
    print("获取借阅信息，用户ID为：", userID)

    # 查询用户
    user = User.objects.get(userID=userID)
    if user:
        # 查询借阅信息
        borrows = Reserve.objects.filter(userID=user)
        borrows_list = list(borrows.values('reserveID', 'bookID__title', 'userID__name', 'startTime', 'DDL'))
        print("借阅信息：", borrows_list)
        # 返回成功响应
        return Response({'success': True, 'borrows': borrows_list})
    else:
        # 返回失败响应，未找到用户
        return Response({'success': False, 'message': '未找到用户'})


def add_quotations(request):
    quote = request.data.get('Quote')  # 获取请求中的引用
    author_name = request.data.get('Author')  # 获取请求中的作者
    print("添加引言：", quote, "，作者为：", author_name)

    # 先判断作者是否存在
    if not Author.objects.filter(name=author_name).exists():
        # 作者不存在，创建作者
        author = Author(
            authorID=Author.generate_author_id(),
            name=author_name,
        )
        author.save()  # 保存作者

    # 提取出作者
    author = Author.objects.get(name=author_name)

    # 创建引言
    quotation = Quotation(
        quotation=quote,
        author=author,
    )
    quotation.save()  # 保存引言
    print("引言添加成功，ID为：", quotation.quotationID)
    # 返回成功响应
    return Response({'success': True})

def get_quotations(request):
    # 查询所有引言
    quotations = Quotation.objects.all()
    quotations_list = list(quotations.values('quotationID', 'quotation', 'author__name'))
    print("所有引言：", quotations_list)
    # 返回成功响应
    return Response({'success': True, 'quotations': quotations_list})

def delete_quotation(request):
    quotationID = request.data.get('quotationID')  # 获取请求中的引言 ID
    print("删除引言，引言 ID 为：", quotationID)

    # 查询引言
    quotation = Quotation.objects.get(quotationID=quotationID)
    if quotation:
        # 删除引言
        quotation.delete()
        # 返回成功响应
        return Response({'success': True})
    else:
        # 返回失败响应，未找到引言
        return Response({'success': False, 'message': '未找到语录'})
    
def search_quotations(request):
    searchInfo = request.data.get('searchInfo')  # 获取请求中的搜索信息
    print("搜索作者/引言：", searchInfo)

    # 查询作者或引言
    quotations = Quotation.objects.filter(
        Q(author__name__icontains=searchInfo) | Q(quotation__icontains=searchInfo)
    )

    quotations_list = list(quotations.values('quotationID', 'quotation', 'author__name'))
    print("搜索结果：", quotations_list)
    # 返回成功响应
    return Response({'success': True, 'quotations': quotations_list})

def edit_quotation(request):
    quotationID = request.data.get('quotationID')  # 获取请求中的引言 ID
    quote = request.data.get('quote')  # 获取请求中的新引用 
    author_name = request.data.get('author_name')  # 获取请求中的新作者
    print("编辑引言，引言 ID 为：", quotationID, "，引用为：", quote, "，作者为：", author_name)

    # 查询引言
    quotation = Quotation.objects.get(quotationID=quotationID)
    if quotation:
        # 查找作者是否存在
        if not Author.objects.filter(name=author_name).exists():
            # 作者不存在，更改失败
            return Response({'success': False, 'message': '作者不存在'})
        # 修改引言信息
        quotation.quotation = quote
        quotation.author = Author.objects.get(name=author_name)
        quotation.save()  # 保存引言
        # 返回成功响应
        return Response({'success': True})
    else:
        # 返回失败响应，未找到引言
        return Response({'success': False, 'message': '未找到语录'})


def send_message(request):
    # 获取请求中的信息
    sender = request.data.get('sender')  # 发送者
    receiver = request.data.get('receiver')  # 接收者
    content = request.data.get('content')  # 内容
    reserveID = request.data.get('reserveID')  # 预定 ID
    print("发送消息，发送者为：", sender, "，接收者为：", receiver, "，借阅编号：", reserveID, "，内容为：", content)

    # 查询接收者
    reserve = Reserve.objects.filter(reserveID=reserveID).first()
    sender_user = Administrator.objects.get(adminID=sender)
    if reserve:
        # 创建消息
        receiver_user = reserve.userID
        message = Message(
            messageID=Message.generate_message_id(),
            sender=sender_user,
            receiver=receiver_user,
            content=content,
            isRead=False,
            time=timezone.now()
        )
        message.save()  # 保存消息
        print("消息发送成功，ID为：", message.messageID)
        # 返回成功响应
        return Response({'success': True})
    else:
        # 返回失败响应，未找到接收者
        return Response({'success': False, 'message': '未找到接收者'})
    
def get_messages(request):
    # 获取请求中的信息
    userID = request.data.get('userID')  # 用户 ID
    print("获取消息，用户 ID 为：", userID)

    # 查询用户
    user = User.objects.get(userID=userID)
    if user:
        # 查询未读消息
        messages = Message.objects.filter(receiver=user)
        messages_list = list(messages.values('messageID','sender__adminID', 'content','time', 'isRead'))
        
        # 格式化时间
        for message in messages_list:
            # 直接使用 datetime 对象格式化时间
            local_time = message['time'].astimezone(timezone.get_current_timezone())
            message['time'] = local_time.strftime('%Y-%m-%d %H:%M:%S')

        
        print("用户消息：", messages_list)
        # 返回成功响应
        return Response({'success': True,'messages': messages_list})
    else:
        # 返回失败响应，未找到用户
        return Response({'success': False, 'message': '未找到用户'})

def delete_message(request):
    # 获取请求中的信息
    messageID = request.data.get('messageID')  # 消息 ID
    print("删除消息，消息 ID 为：", messageID)

    # 查询消息
    message = Message.objects.get(messageID=messageID)
    if message:
        # 删除消息
        message.delete()
        # 返回成功响应
        return Response({'success': True})
    else:
        # 返回失败响应，未找到消息
        return Response({'success': False, 'message': '未找到消息'})


