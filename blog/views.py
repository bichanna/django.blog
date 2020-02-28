from django.shortcuts import render

# Create your views here.



"""
Blogアプリ
表示用の機能作成

Filename  views.py
Date: 2020.2.21
Written by Nobuharu Shimazu

"""
from django.shortcuts import render
from django.views.generic import View,DetailView
from django.utils import timezone
from .models import Post

class PostListView(View):
	def get(self,request,*args,**kwarge):
		"""
			Get request用の処理
			ブログ記事入欄を表示する
		"""
		context = {}
		#記事データを取得
		posts = Post.objects.filter(published_date__lte=timezone.now()).order_by("published_date")
		context["posts"] = posts
		return render(request,"blog/post_list.html",context)

post_list = PostListView.as_view()

class PostDetailView(DetailView):
	model = Post
	template_name = "blog/post_detail.html"


post_detail = PostDetailView.as_view()