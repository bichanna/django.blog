"""
	Accounts 更新フォームの定義

	Filename forms.py
	Date: 2020.4.6
	Written by Nobuharu Shimazu
"""

from django.forms import ModelForm
from django.contrib.auth.models import User
class UserUpdateForm(ModelForm):
	"""ユーザー情報更新フォーム"""
	class Meta:
		model = User
		fields = ("last_name", "first_name",)


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			field.widget.attrs["class"] = "form-control"