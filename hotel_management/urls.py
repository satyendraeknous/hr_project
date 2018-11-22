from django.conf.urls import url
from django.conf.urls.static import static
from . import views





urlpatterns = [
    
    #url(r'^hotel_home/$', views.hotel_home, name='hotel_home'),
    url(r'^hotel_search/$', views.hotel_search, name='hotel_search'),
    url(r'^(?P<pk>[^/]+)/hotel_register/$', views.hotel_register, name='hotel_register'),
    url(r'^conform_email/$', views.conform_email, name='conform_email'),
    url(r'^invalid_email/$', views.invalid_email, name='invalid_email'),
    url(r'^(?P<pk>[^/]+)/hotel_search_details/', views.hotel_details, name='hotel_search_details'),
    url(r'^hotel_dashboard/$', views.hotel_dashboard, name='hotel_dashboard'),
    url(r'^(?P<pk>[^/]+)/hotel_dashboarddetails/$',
        views.hotel_dashboarddetails, name='hotel_dashboarddetails'),
    url(r'^hotel_dashboardcreate/$', views.hotel_dashboardCreate, name='hotel_dashboardcreate'),
    url(r'^(?P<pk>[^/]+)/hotel_dashboardupdate/$', views.hotel_dashboardUpdate, name='hotel_dashboardupdate'),

    url(r'^(?P<pk>\d+)/hotel_dashboarddelete/$',
        views.Hotel_dashboardDelete, name='hotel_dashboarddelete'),


    url(r'^(?P<pk>[^/]+)/hotel_dashboardhoteldetail/$', views.hotel_dashboardhoteldetail, name='hotel_dashboardhoteldetail'),



    #--------url for OTP send-------->
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),

    #--------End url for OTP send-------->


]