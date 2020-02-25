"""
	Blogアプリ
	URL定義

	Filename  urls.py
	Date:2020.2.21
	Written by Nobuharu Shimazu

"""
from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
	path("",views.post_list, name="post_list"),
]