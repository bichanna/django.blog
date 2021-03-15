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
	class Meta:
		model = Post
		fields = ("title", "text", "image")
		labels = {
			"title":"Title",
			"text":"Text",
			"image":"Image",
		}

class PostSearchForm(forms.Form):
	key_word = forms.CharField(
		required=False,
		widget= forms.TextInput(attrs={"placeholder":"🔍 search..."})   # this is how to put a place holder
        )


#🔍 search...