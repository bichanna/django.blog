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
from django.template.defaultfilters import slugify


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
	likes= models.IntegerField(default=0)
	dislikes = models.IntegerField(default=0)
	url = models.SlugField(max_length=300, default=False)


	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def save(self, *args, **kwargs):
		self.url= slugify(self.title)
		super(Post, self).save(*args, **kwargs)
		

	def __str__(self):
		return str(self.author) + " " + str(self.title)



class Preference(models.Model):
	user= models.ForeignKey(User, on_delete=models.CASCADE)
	post= models.ForeignKey(Post, on_delete=models.CASCADE)
	value= models.IntegerField()
	date= models.DateTimeField(auto_now= True)

	def __str__(self):
		return str(self.user) + ":" + str(self.post) + ":" + str(self.value)

	class Meta:
		unique_together = ("user", "post", "value")

















