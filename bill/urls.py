from django.conf.urls import url
from . import views

urlpatterns = [
			url(r'^$', views.user_login, name='login'),
			url(r'^register/$', views.register, name='register'),
			url(r'^logout/$',views.logout, name='logout'),
			url(r'^Print_PDF/(?P<pk>\d+)/$', views.print_pdf, name='print_pdf'),
			url(r'^place_order/$', views.place_order, name='place_order'),
			url(r'^PDF/(?P<pk>\d+)/$', views.pdf_view, name='pdf_view')
		]