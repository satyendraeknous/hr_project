from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from sycco_management.views import *


urlpatterns = [
    
    
    url(r'^$', Sycco_Home.as_view(), name='sycco_home'),
    url(r'^sycco_registration/$', Sycco_Registration.as_view(), name='sycco_registration'),
    url(r'^sycco_dashboard/$', Sycco_Dashboard.as_view(), name='sycco_dashboard'),
    url(r'^sycco_dashboardcreate/$', Sycco_DashboardCreate.as_view(), name='sycco_dashboardcreate'),

    url(r'^(?P<pk>\d+)/sycco_dashboardupdate/$',
        Sycco_DashboardUpdate.as_view(), name='sycco_dashboardupdate'),

    url(r'^(?P<pk>\d+)/sycco_dashboarddetail/$',
        Sycco_DashboardDetail.as_view(), name='sycco_dashboarddetail'),

    url(r'^(?P<pk>\d+)/sycco_dashboarddelete/$',
        Sycco_DashboardDelete.as_view(), name='sycco_dashboarddelete'),
    
    
]