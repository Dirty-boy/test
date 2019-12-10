from django.shortcuts import redirect, HttpResponse, render
from django.utils.deprecation import MiddlewareMixin



class My_Cookie(MiddlewareMixin):
	def process_request(self, request):
		print(f'cookie内容:{request.COOKIES}')
		print('-------------------------------')
		print(f'POST内容:{request.POST}')
		print('--------------------------------')
		print(f'GET:>>>{request.GET}')
		white_list = ['login',]
		print('----------------------------------')
		print(f'path>>>>>>>>>>{request.path}')
		path = request.path
		path = path.split('/')[1]
		if path in white_list:
			pass
		else:
			order = request.COOKIES.get('allow')
			if order == 'True' and request.COOKIES.get('sessionid'):
				pass
			else:
				return redirect('login:login')