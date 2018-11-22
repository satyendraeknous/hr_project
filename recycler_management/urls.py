from django.conf.urls import url
from recycler_management.views import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^recycler_home/$', Recycler_Home.as_view(), name = 'recycler_home'),
    #url(r'^recycler_registration/$', Recycler_Registeration.as_view(), name = 'recycler_registration'),
    url(r'^recycler_dashboard/$', Recycler_Dashboard.as_view(), name = 'recycler_dashboard'),
    url(r'^(?P<pk>\d+)/recycler_dashboarddetail/$', Recycler_Dashboarddetail.as_view(), name='recycler_dashboarddetail'),
    url(r'^(?P<pk>\d+)/recycler_dashboardupdate/$', RecyclerUpdateView.as_view(), name='recycler_dashboardupdate'),


    url(r'^(?P<pk>\d+)/recycler_dashboardgreendetail/$', Recycler_Dashboardgreendetail.as_view(), name='recycler_dashboardgreendetail'),


]