from django.contrib import admin
from .models import Author, Bookshelf, Administrator, User, Lend, Reserve, Backgroud, Quotation, Message

admin.site.register(Author)
admin.site.register(Bookshelf)
admin.site.register(Administrator)
admin.site.register(User)
admin.site.register(Lend)
admin.site.register(Reserve)
admin.site.register(Backgroud)
admin.site.register(Quotation)
admin.site.register(Message)