from django.conf.urls import url,include
from main import views

urlpatterns = [
	url(r'^$',views.Main.as_view(),name='main'),
	url(r'^add/(\d+)/',views.Labor.as_view(),name='alter'),
	url(r'^add/',views.Labor.as_view(),name='labor'),
	url(r'see/',views.SeeAll.as_view(),name='select'),
	url(r'see/(\w+)/',views.SeeAll.as_view(),name='person_select'),
	url(r'^change/',views.Batch_convert.as_view(),name='changed'),
]