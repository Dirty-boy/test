from django.shortcuts import render,redirect,reverse
from main import models
# Create your views here.
from django import views

class Login(views.View):
	def get(self,request):
		return render(request,'login/login.html')
	def post(self,request):
		data = request.POST.dict()
		var = models.Userinfo.objects.filter(username=data['username'],password=data['password']).values()
		if bool(var) is False:
			return render(request,'login/login.html',{'error':'未注册用户'})
		else:
			ret = redirect(reverse('main:main'))
			ret.set_cookie('allow','True')
			request.session['user_name'] = data['username']
			return ret



class Register(views.View):
	def get(self,request):
		return render(request,'login/register.html')
	def post(self,request):
		dic = request.POST.dict()
		print(f'dic内容:{dic}')
		user_name = dic['username']
		num = models.Userinfo.objects.filter(username=user_name).values('id')
		if  bool(num) is False:
			print('跳转页面')
			models.Userinfo.objects.create(username=user_name,password=dic['password'],telephone=dic['phone_number'],email=dic['email'])
			ret = redirect(reverse('main:main'))
			ret.set_cookie('allow','True')
			request.session['user_name'] = user_name
			return ret
		else:
			return render(request,'login/register.html',{"error":"用户名重复"})





class Login_bms(views.View):
	def get(self,request):
		return render(request,'login/login&bms.html')
