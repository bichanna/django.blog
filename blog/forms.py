"""
	Blogアプリ
	フォームクラス
	Filename forms.py
	Date: 2020.4.27
	Written by Nobuharu Shimazu
"""


from django.forms import ModelForm
from django import forms
from .models import Post

class PostForm(ModelForm):
	"""
		記事登録画面用のフォーム
		title: ブログのタイトル
		text: ブログ本文
	"""
	class Meta:
		#モデルクラスを指定
		model = Post
		#モデルフィールドを指定
		fields = ("title", "text")
		labels = {
			"title":"タイトル",
			"text":"テキスト",
		}

class PostSearchForm(forms.Form):
	"""
		記事検索用のフォーム
	"""
	key_word = forms.CharField(label="検索キーワード", required=False)