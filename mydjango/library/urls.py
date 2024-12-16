from django.urls import path
from .views import handle_post

urlpatterns = [
    path('post/', handle_post, name='post'),
]