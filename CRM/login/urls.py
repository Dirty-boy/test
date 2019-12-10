from django.conf.urls import url,include
from login import views

urlpatterns = [
	url(r'^$',views.Login.as_view(),name='login'),
	url(r'^bms/',views.Login_bms.as_view(),name='login_bms'),
	url(r'^register/',views.Register.as_view(),name='register')
]