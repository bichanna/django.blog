"""
	Accounts 更新フォームの定義

	Filename forms.py
	Date: 2020.4.6
	Written by Nobuharu Shimazu
"""

from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserUpdateForm(ModelForm):
	"""ユーザー情報更新フォーム"""
	class Meta:
		model = User
		fields = ("username","email","first_name", "last_name")


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			field.widget.attrs["class"] = "form-control"

class UserCreateForm(UserCreationForm):
	"""
		ユーザー作成用フォーム
	"""
	class Meta(UserCreationForm.Meta):
		fields = ("username", "email")