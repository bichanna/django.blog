from django.shortcuts import render

# Create your views here.



"""
Blogアプリ
表示用の機能作成

Filename  views.py
Date: 2020.2.21
Written by Nobuharu Shimazu

"""
from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic import View,DetailView, CreateView, RedirectView, UpdateView, DeleteView, ListView
from django.utils import timezone
from .models import Post
from .forms import PostForm, PostSearchForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect

class PostHomeView(ListView):
	model = Post
	template_name = "blog/post_home.html"

post_list = PostHomeView.as_view()

class PostListView(ListView):
	"""
		Get Request用の処理
		ブログ記事一覧を表示する。
	"""
	model = Post
	template_name = "blog/post_list.html"
	paginate_by = 6



	def get_queryset(self):
		"""
			検索条件の設定
		"""
		#フォームを設定。
		#user = self.request.user
		#if user.is_authenticated:
		form = PostSearchForm(self.request.GET or None)
		self.form = form
		sort = self.request.GET.get('sort')
		if sort == "old":
			queryset = super().get_queryset()
		else:
			queryset = super().get_queryset()
			queryset = queryset.order_by("-published_date")
	
		if form.is_valid():
			key_word = form.cleaned_data.get('key_word')
			if key_word:
				for word in key_word.split():
					queryset = queryset.filter(Q(title__icontains=word) | Q(text__icontains=word))




		#記事データを取得
		queryset = queryset.filter(published_date__lte=timezone.now())
		return queryset
		"""
		else:
			form = PostSearchForm(self.request.GET or None)
			self.form = form
			queryset = super().get_queryset()
			queryset = queryset.filter(author_id__username=self.request.user.username)
			return queryset
		"""



	def get_context_data(self, **kwargs):
		"""
			コンテキストの設定。
		"""

		context = super().get_context_data(**kwargs)
		context["form"] = self.form
		return context

post_list = PostListView.as_view()

class AboutView(ListView):
	model = User
	template_name = "blog/about.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["users"] = len(User.objects.all())
		return context

post_list = AboutView.as_view()


class PostDetailView(DetailView):
	model = Post
	template_name = "blog/post_detail.html"

	def get_queryset(self):
		queryset = super().get_queryset()
		if self.kwargs['pk']:
			return Post.objects.filter(id=self.kwargs["pk"])
		else:
   			return Post.objects.none()
   			
	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context["latest"] = "/"+str(len(Post.objects.all()))+"/"
		print("⭐"*10)
		print(context["latest"])
		return context
	
	
post_detail = PostDetailView.as_view()



class PostCreateView(LoginRequiredMixin, CreateView):
	"""
		ブログ記事作成用のビュー

	"""
	model = Post
	form_class = PostForm
	template_name = "blog/post_add.html"

	def form_valid(self, form):
		form.instance.author = self.request.user

		return super().form_valid(form)

	def get_success_url(self):
		"""
			詳細画面にリダイレクトする。
		"""
		return reverse('blog:post_detail', args=(self.object.id,))# argsのカッコはタプルにしなきゃいけないから、一つでもカンマをつける。





class PostReviewListView(LoginRequiredMixin, View):
	"""
		下書き一覧のページ
	"""
	def get(self, request, *args, **kwargs):
		"""
			ブログの下書き記事一覧を表示する。
		"""
		context = {} #postsから取ってきたテンプレートで使うデータが入ってる。
		# 記事データを取得
		posts = Post.objects.filter(author=self.request.user, published_date__isnull=True).order_by("created_date")
		context["posts"] = posts
		return render(request, "blog/review_list.html",context)


class PublishRedirectView(LoginRequiredMixin, RedirectView):
	"""
		詳細ページでpublishに変更するボタンを押した時にリダイレクトして一覧に戻す。
	"""
	pattern_name = "blog:post_detail"
	def get_redirect_url(self, *args, **kwargs):
		post = get_object_or_404(Post, pk=kwargs['pk'])
		post.publish()
		return super().get_redirect_url(*args, **kwargs)



class PostUpdateView(LoginRequiredMixin, UpdateView):
	"""
		変更ページのビュー
	"""
	model = Post
	form_class = PostForm
	template_name = 'blog/post_update.html'

	def get_success_url(self):
		"""詳細画面にリダイレクトする。"""
		return reverse('blog:post_detail', args=(self.object.id,))


class PostDeleteView(LoginRequiredMixin, DeleteView):
	"""
		削除用のビュー
	"""
	model = Post
	template_name = "blog/post_delete.html"
	def get_success_url(self):
		"""一覧ページにリダイレクト"""
		return reverse("blog:post_list")





