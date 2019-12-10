from django import forms
from main import models
from django.core.exceptions import  ValidationError

class Main_Form(forms.ModelForm):
	"""
	添加页面函数
	"""
	class Meta:
		model = models.Customer
		fields = '__all__'
		exclude = ['delete_status',]


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for name, field in self.fields.items():
			if name == 'course':
				continue

			field.widget.attrs.update({'class': 'form-control'})

