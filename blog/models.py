from django.db import models

# Create your models here.
"""
Blogアプリ
データモデル

FIle name   model.py
date: 2020.2.2.19
Written by Nobuharu Shimazu

"""
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
	"""
		ブログ記事クラス

		author: さくしゃ (Djangoのユーザモデルを利用)
		title: ブログのタイトル
		text: ブログ本文
		created_date: 作成日
		published_date: 公開日
	"""
	#フィールドの定義
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(default = timezone.now)
	published_date = models.DateTimeField(blank=True,null=True)
	image = models.ImageField(upload_to="images", blank=True, null=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return str(self.author) + " " + str(self.title)





















