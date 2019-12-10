from django.shortcuts import render,redirect,HttpResponse,reverse
from django.views import View
from main import models
# Create your views here.
from django.db.models import Q
class Main(View):
	"""
	主页
	"""
	def get(self,request):
		data = request.session.get('user_name')
		return render(request,'main/main.html',{'name':data})

from main import Model_Form
class Labor(View):
	"""
	添加页面
	"""
	def get(self,request,id=None):
		name = request.session.get('user_name')
		goods = Model_Form.Main_Form(instance=models.Customer.objects.filter(id=id).first())
		print(goods)
		return render(request,'main/labor_union.html',{'msg':goods,'name':name})
	def post(self,request,cid,*args,**kwargs):
		name = request.session.get('user_name')
		dic = request.POST.dict()
		yes = Model_Form.Main_Form(request.POST,instance=models.Customer.objects.filter(id=cid).first())
		if yes.is_valid():
			yes.save()
		return redirect('main:select')

from main import paging as P
class SeeAll(View):
	def get(self,request):
		name = request.session.get('user_name')
		sarg = request.GET.dict()
		if len(sarg) > 1:
			action = sarg[ 'action' ]
			kw = sarg[ 'kw' ]
			if kw and action:
				q = Q()
				q.children.append([ action, kw ])
				data = models.Customer.objects.filter(q)
				One = P.paging(data, sarg)
				msg = One.show()
				low = One.html()
				return render(request, 'main/select_page.html', {'msg': msg, 'name': name, "low": low,'tag':1})
		elif request.path == '/main/see/':
			data = models.Customer.objects.filter(delete_status=False,consultant=None)
			One = P.paging(data, sarg)
			msg = One.show()
			low = One.html()
			return render(request, 'main/select_page.html', {'msg': msg, 'name': name, "low": low,'tag':1})
		else:
			use = request.path.split('/')[3]
			data = models.Customer.objects.filter(delete_status=False,consultant__username=use)
			One = P.paging(data, sarg)
			msg = One.show()
			low = One.html()
			return render(request, 'main/select_page.html', {'msg': msg, 'name': name, "low": low})

	def post(self,request):
			print(f'当前页面:!@!!##!#!#{request.POST}')
			request.session.flush()
			ret = redirect('login:login')
			ret.delete_cookie('allow')
			return redirect(reverse('login:login'))

class Batch_convert(View):
	def get(self,request):
		print(f'get>>>:{request.GET}')
	def post(self,request):
		print(f'!!!!!!!!!!!!!!!!!post:>>>>>>>{request.POST}')
		try:
			order = request.POST.get('pcpr')
			if order is None:
				assert False
			#公户转私户
			name = request.session.get('user_name')
			cid = request.POST.getlist('cids')

			for i in  cid:
				models.Customer.objects.filter(id=int(i),consultant__isnull=True).update(consultant=models.Userinfo.objects.filter(username=name).first())
			return redirect(reverse('main:person_select',args=(name,)))
		except Exception:
			order = request.POST.get('prcp')
			cid = request.POST.getlist('cids')
			for i in cid:
				print(i)
				models.Customer.objects.filter(id=int(i)).update(consultant=None)
			return redirect('main:select')
