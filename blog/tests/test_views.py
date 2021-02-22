"""
	blogアプリ
	viewのテスt

	Filename test_views.py
	Date: 2020.9.8
	Written by Nobu
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from blog.models import Post

User = get_user_model()

class PostDetailViewTests(TestCase):
	"""
		PostDetailViewのテスト
	"""
	def setUp(self):
		super().setUp()
		self.client = Client()  #テスト用のクライアント

		#ユーザー作成
		self.username = "foo@hoge.com"
		self.password = "secret"
		user = User.objects.create_user(username = self.username,password=self.password)

		self.username2 = "bar[hoge.com"
		self.password2 = "secret"
		user2 = User.objects.create_user(username=self.username2,password=self.password2)
		
		#下書き記事作成
		self.post = Post.objects.create(author=user,title="test",text="test")
		
		#公開記事作成
		self.post2 = Post.objects.create(author=user,title="test2",text="test2")
		self.post2.publish()

		#別ユーザーの記事作成
		self.post3 = Post.objects.create(author=user2,title="test3",text="test3")

		
		#詳細ページのパスを作成
		#下描き記事
		self.path = reverse("blog:post_detail",args=(self.post.id,))
		
		#公開記事
		self.path2 = reverse("blog:post_detail",args=(self.post2.id,))

		#別ユーザーの記事
		self.path3 = reverse("blog:post_detail",args=(self.post3.id,))	

	def test_superuser_logged_in(self):
		"""ログイン済みでスーパーユーザーが他人の記事を閲覧"""
		#スーパーユーザー
		username = "superman"
		password = "super"
		superuser = User.objects.create_superuser(username=username,password=password)

		#ユーザーを作成しログイン
		self.client.login(username=username,password=password)

		#テスト対象を実行
		res = self.client.get(self.path3)

		#スーパーユーザーがログインする場合は常に閲覧可のう
		self.assertEqual(res.status_code,200)



	def test_published_not_logged_in(self):
		"""ログインしていない公開記事の場合のテスト"""
		
		#テスト対象を実行
		res = self.client.get(self.path2)
		
		#記事は見られる
		self.assertEqual(res.status_code,200)


class PostReviewListViewTests(TestCase):
	"""
		下書き一覧ページのテスト
	"""
	def setUp(self):
		super().setUp()
		self.client = Client()

		#ユーザー作成
		self.username = "foo@hoge.com"
		self.password = "secret"
		user = User.objects.create_user(username=self.username,password=self.password)

		#下書き記事作成
		self.post = Post.objects.create(author=user,title="test",text="test")

		#下書き一覧ページ
		self.path = reverse("blog:post_review")

	def test_myport_not_logged_in(self):
		"""ログインしていない状態で自分の下書き一覧を表示"""
		#テスト対象を実行
		res = self.client.get(self.path)

		#自分の記事は閲覧可能
		self.assertEqual(res.status_code,302)

class PostCreateViewTests(TestCase):
	"""
		記事作成ページのテスト
	"""
	def setUp(self):
		super().setUp()
		self.client = Client()

		#ユーザー作成
		self.username = "foo@hoge.com"
		self.password = "secret"
		user = User.objects.create_user(username=self.username,password=self.password)

		#記事追加
		self.path = reverse("blog:post_add")

	def test_logged_in(self):
		"""ログインしたときに表示"""
		#ユーザーログイン
		self.client.login(username=self.username,password=self.password)

		#テスト対象を実行
		res = self.client.get(self.path)

		#表示可能
		self.assertEqual(res.status_code,200)

	def test_not_logged_in(self):
		"""ログインしていないときはリダイレクト"""
		#テスト対象を実行
		res = self.client.get(self.path)

		#ログインぺーじにリダイレクト
		self.assertEqual(res.status_code,302)

	def test_post_null(self):
		"""からのデータできじ作成"""
		#ユーザーログイン
		self.client.login(username=self.username,password=self.password)

		data = {}
		res = self.client.post(self.path,data=data)
		#成功しない場合は同じページを表示
		self.assertEqual(res.status_code,200)

	def test_post_with_data(self):
		"""記事を登録する"""
		#ユーザーログインん
		self.client.login(username=self.username,password=self.password)
		data = {
			"title":"こんにちは",
			"text":"ようこそ",
		}
		res = self.client.post(self.path,data=data)
		#成功すればリダイレクト
		self.assertEqual(res.status_code,302)



class PostUpdateViewTests(TestCase):
	"""
		更新ページのテスト
	"""
	def setUp(self):
		super().setUp()
		self.client = Client()

		#ユーザー作成
		self.username = "foo@hoge.com"
		self.password = "secret"
		user = User.objects.create_user(username = self.username,password=self.password)

		#記事作成
		self.post = Post.objects.create(author=user,title="test",text="test")
		self.post.publish()

		#一覧ページ
		self.path = reverse("blog:post_update",args=(3432,))
		self.path2 = reverse("blog:post_update",args=(self.post.id,))

	def test_update_not_exsisting_post(self):
		"""
			存在しない記事IDで表示する場合、404になる。
		"""
		self.client.login(username=self.username,password=self.password)
		res = self.client.get(self.path)
		self.assertEqual(res.status_code,404)

	def test_after_update_goto_detailpage(self):
		"""
			更新時に詳細ページにリダイレクトされる
		"""
		self.client.login(username=self.username,password=self.password)
		data = {
			"title":"こんにちは",
			"text":"ようこそ",
		}
		res = self.client.post(self.path2,data=data)
		self.assertEqual(res.status_code,302)


class PostDeleteViewTests(TestCase):
	"""
		削除ページのテスト
	"""
	def setUp(self):
		super().setUp()
		self.client = Client()

		#ユーザー作成
		self.username = "foo@hoge.com"
		self.password = "secret"
		user = User.objects.create_user(username = self.username,password=self.password)

		#記事作成
		self.post = Post.objects.create(author=user,title="test",text="test")
		self.post.publish()

		#パスを作成
		self.path = reverse("blog:post_delete",args=(self.post.id,))
		self.path2 = reverse("blog:post_delete",args=(28883849493,))

	def test_after_delete_post_goto_postlist(self):
		"""
			想定通り削除してリダイレクトされる
		"""
		self.client.login(username=self.username,password=self.password)
		res = self.client.post(self.path)
		self.assertEqual(res.status_code,302)

	def test_delete_not_exsisting_postID(self):
		"""
			存在しない記事IDで確認ページを表示する場合、404になる
		"""
		self.client.login(username=self.username,password=self.password)
		res = self.client.post(self.path2)
		self.assertEqual(res.status_code,404)



class PostPublishRedirectView(TestCase):
	"""
		#公開ボタンのテスト
	"""
	def setUp(self):
		super().setUp()
		self.client = Client()

		#ユーザー作成
		self.username = "foo@hoge.com"
		self.password = "secret"
		user = User.objects.create_user(username = self.username,password=self.password)

		#記事作成
		self.post = Post.objects.create(author=user,title="test",text="test")

		#パス作成
		self.path = reverse("blog:publish",args=(self.post.id,))
		self.path2 = reverse("blog:publish",args=(238489,))

	def test_goto_404_if_there_is_noresorce(self):
		"""
			#リソースがない場合は404になる
		"""
		self.client.login(username=self.username,password=self.password)
		res = self.client.get(self.path2)
		self.assertEqual(res.status_code,404)

	def test_after_publish_thepost_goto_postlist(self):
		"""
			#押したときのページが想定通りリダイレクトする
		"""
		self.client.login(username=self.username,password=self.password)
		res = self.client.post(self.path, publish="publish")
		self.assertEqual(res.status_code,302)



class PostListViewTests(TestCase):
	"""
		#記事一覧
	"""
	def setUp(self):
		super().setUp()
		self.client = Client()

		#ユーザー作成
		self.username = "foo@hoge.com"
		self.password = "secret"
		user = User.objects.create_user(username = self.username,password=self.password)

		#記事作成
		self.post1 = Post.objects.create(author=user,title="test1",text="test1")
		self.post2 = Post.objects.create(author=user,title="test2",text="test2")
		self.post1.publish()
		self.post2.publish()

		#パス作成
		self.path = reverse("blog:post_list")


	def test_after_serched_it_would_change(self):
		"""
			#検索した場合と検索していない場合のリストの中身が変化する
		"""
		#ユーザーログイン
		self.client.login(username=self.username,password=self.password)
		data = {
			"key_word":"test1"
		}
		res = self.client.get(self.path, data=data)
		self.assertEqual(res.status_code,200)
		self.assertQuerysetEqual(
			res.context["post_list"], ["<Post: foo@hoge.com test1>"]
		)


















