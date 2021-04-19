"""
	Blogアプリ
	URL定義

	Filename  urls.py
	Date:2020.2.21
	Written by Nobuharu Shimazu

"""
from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib import admin

app_name = "blog"
urlpatterns = [
	path("",views.PostHomeView.as_view(), name="post_home"),
	path("posts",views.PostListView.as_view(), name="post_list"),
	path("posts/<int:pk>/",views.post_detail, name="post_detail"),
	path("add/",views.PostCreateView.as_view(),name="post_add"),
	path("review/",views.PostReviewListView.as_view(),name="post_review"),
	path("about.../",views.AboutView.as_view(), name="about..."),
	path("posts/<int:pk>/publish/",views.PublishRedirectView.as_view(),name="publish"),
	path("posts/<int:pk>/update/", views.PostUpdateView.as_view(), name="post_update"),
	path("posts/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
	
]