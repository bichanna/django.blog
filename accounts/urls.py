"""
	Accounts アプリ
	URL 定義

	Filename urls.py
	Date: 2020,4,6
	Written by Nobuharu Shimazu

"""

from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
	path("profile/<int:pk>",views.UserDetail.as_view(),name ="user_detail"),
	path("profile/update/<int:pk>",views.UserUpdate.as_view(),name = "user_update")
]