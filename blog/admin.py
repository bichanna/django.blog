"""
Blogアプリ
admin用の設定

Filename admin.py
Date: 2020.2.19
Written by Nobuharu Shimazu
"""
from django.contrib import admin
from .models import Post


admin.site.register(Post)





### adminのパスワードはNobu8717
