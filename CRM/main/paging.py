
from main import models
from django.urls import reverse
from django.db.models import Q

class paging:
	def __init__(self,data,sarg,max_page_count=20,sum_file_count = 7):
		self.data = data   #传入的未筛选过的数据
		data_count = self.data.values().count()   #计算数据总条数
		self.max_page_count = max_page_count  #每页最大显示数量
		self.sum_file_count = sum_file_count	 #分页显示页数

		self.sarg = sarg   #查询参数
		# print(f'查询参数:{self.sarg}')
		# print(f'数据:{self.data}')
		try:
			page_num = self.sarg[ 'page' ]
			self.now_page = int(page_num)
		except Exception:
			self.now_page = 1
		# print(f'pagenum>>>>>{self.now_page}')
		#-----------判断最大分页数---------------#
		a,b = divmod(data_count,self.max_page_count)
		if b != 0:
			self.all_page = a+1
		else:
			self.all_page = a
		#-------------输出的为最大分页数a----------------#

		#-判断当前页面访问是否正常,如不正常则默认为1--------#
		try:
			now_page = int(self.now_page)
		except Exception:
			now_page = 1
		#----------输出结果默认为1,或1以上的内容-----------#

		#----------当前页数不能大于总页数,也不能小于1-------#
		if 1<= now_page <= self.all_page:
			pass
		elif now_page <= 1:
			now_page = 1
		elif now_page >= self.all_page:
			now_page = self.all_page
		#---------输出结果为正常结果或1或最大页数----------#

		#---------显示当前的渲染页码数--------------------#
		num = self.sum_file_count //2 #前后页码数一致

		end_page = now_page + num
		start_page = now_page - num
		if start_page < 1:
			start_page = 1
			end_page = start_page+self.sum_file_count
		else:
			end_page = self.all_page
			start_page = end_page -self.sum_file_count
		self.now_page_list = range(start_page, end_page)
		if self.all_page <= self.max_page_count:
			self.now_page_list = range(1,self.all_page+1)
		# print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>当前页数:{self.now_page_list}")
		#----------生成显示的页码列表now_page_list--------#


	def show(self):
		# --------根据参数来筛选数据--------------#
		if bool(self.sarg) is False:
			# print('没有输入任何参数,默认为首页,nowpage=1')
			data = self.data[0:self.max_page_count]
			return data
		elif len(self.sarg.keys()) == 1:
			# print(f'拥有一个参数的时候')
			try:
				page = int(self.sarg['page'])
			except Exception:
				page = 1
			data = self.data[self.max_page_count*(page-1):self.max_page_count*page]
			return data
		else:
			try:
				page = int(self.sarg['page'])
			except Exception:
				page = 1
			data = self.data[self.max_page_count*(page-1):self.max_page_count*page]
			return data
	def html(self):

		# print('没有输入任何参数,默认为首页,nowpage=1')
		sary = ''
		if len(self.sarg) > 1:
			sary = 'action=' + self.sarg[ 'action' ] +'&'+ 'kw=' + self.sarg[ 'kw' ]
		"""
		渲染页面
		:return:
		"""
		Head_page = """
				<nav aria-label="Page navigation example">
		  <ul class="pagination">
		"""
		#----------标签头--------#
		# ?action = name__contains & kw = 方伯仁 & page = 7
		One_page = f'''
					<li class="page-item">
					  <a class="page-link" href="?{sary+'&page=1'}" aria-label="Previous">
						<span aria-hidden="true">首页</span>
					  </a>
					</li>
			'''
		#---------首页-----------#
		if self.now_page == 1:
			order = 'disabled'
			# ?action=qq__contains&kw=151
			file = sary+f'&page=1'
		else:
			order = ""

			file = sary+f'&page={self.now_page-1}'
		# print(f'>>>>>>>>>>>>>>>>>>>>>.{self.now_page}<<<<<<<<<<<<<<<<<<<<<')
		Two_page = f'''
						<li class="page-item {order}">
						  <a class="page-link" href="?{file}" aria-label="Previous">
							<span aria-hidden="true">&laquo;</span>
						  </a>
						</li>
				'''
		#----------上一页---------#
		main_page = ''
		for i in self.now_page_list:
			file = f'&page={i}'
			if i == self.now_page:
				light = 'active'
			else:
				light = ' '
			file = sary+f'&page={i}'
			main_page += f'''<li class="page-item" {light}><a class="page-link" href="?{file}">{ i }</a></li>'''
		#-----------显示的主标签-----#
		if self.now_page == self.all_page:
			order = 'disabled'
			file =  sary+f'&page={self.all_page}'
		else:
			order = ""
			file = sary+f'&page={self.now_page+1}'
		next_page = f'''
								<li class="page-item {order}">
								  <a class="page-link" href="?{file}" aria-label="Next">
									<span aria-hidden="true">&raquo;</span>
								  </a>
								</li>
						'''
		#-------------下一页----------#

		last_page = f'''
								   <li class="page-item">
									 <a class="page-link" href="?{sary}&page={self.all_page}" aria-label="Next">
									   <span aria-hidden="true">尾页</span>
									 </a>
								   </li>
								   </ul>
							   </nav>
						   '''
		all_page = Head_page+One_page+Two_page+main_page+next_page+last_page
		return all_page