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
	path("post/<int:pk>/",views.post_detail, name="post_detail"),
	path("post/add/",views.PostCreateView.as_view(),name="post_add"),
	path("post/review/",views.PostReviewListView.as_view(),name="post_review"),
	path("post/<int:pk>/publish/",views.PublishRedirectView.as_view(),name="publish"),
]