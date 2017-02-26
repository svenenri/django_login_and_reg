from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^process/login/(?P<id>\d+)$', views.success, name='login_reg_success'),
	url(r'^process$', views.process, name='login_reg_process'),
	url(r'^$', views.index, name='login_reg_index'),
]
