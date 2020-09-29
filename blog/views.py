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
from .mixins import CheckPermissionMixin


class PostListView(ListView):
	"""
		Get Request用の処理
		ブログ記事一覧を表示する。
	"""
	model = Post
	template_name = "blog/post_list.html"
	paginate_by = 5


	def get_queryset(self):
		"""
			検索条件の設定
		"""
		#フォームを設定。
		form = PostSearchForm(self.request.GET or None)
		self.form = form



		queryset = super().get_queryset()
		if form.is_valid():
			key_word = form.cleaned_data.get('key_word')
			if key_word:
				for word in key_word.split():
					queryset = queryset.filter(Q(title__icontains=word) | Q(text__icontains=word))

		#記事データを取得
		queryset = queryset.filter(published_date__lte=timezone.now()).order_by("published_date")
		print(queryset)
		print(form)
		return queryset


	def get_context_data(self, **kwargs):
		"""
			コンテキストの設定。
		"""
		context = super().get_context_data(**kwargs)
		context["form"] = self.form
		return context

post_list = PostListView.as_view()



class PostDetailView(CheckPermissionMixin,DetailView):
	model = Post
	template_name = "blog/post_detail.html"


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















