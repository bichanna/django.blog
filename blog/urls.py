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
	path("",views.PostListView.as_view(), name="post_list"),
	path("post/<int:pk>/",views.post_detail, name="post_detail"),
	path("post/add/",views.PostCreateView.as_view(),name="post_add"),
	path("post/review/",views.PostReviewListView.as_view(),name="post_review"),
	path("post/about-author/",views.AboutAuthorView.as_view(), name="about_author"),
	path("post/<int:pk>/publish/",views.PublishRedirectView.as_view(),name="publish"),
	path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="post_update"),
	path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
]