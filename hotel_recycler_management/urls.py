"""hotel_recycler_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from . import views
from . import forms
from django.contrib.auth import views as auth_views

import hotel_management
import recycler_management
#from recycler_management.views import *


urlpatterns = [
    url(r'^$', views.user_login, name="user_login"),
    url(r'^admin/', admin.site.urls),
    url(r'^hotel_management/', include('hotel_management.urls'), name='hotel_management'),
    url(r'^recycler_management/', include('recycler_management.urls'), name='recycler_management'),
    url(r'^sycco_management/', include('sycco_management.urls'), name='sycco_management'),

    url(r'^mvp/$', views.mvp, name="mvp"),
    url(r'^user_logout/$', views.user_logout, name="user_logout"),
    url(r'^user_registration/$', views.user_registration, name="user_registration"),
    url(r'^user_passwordchange/$', views.user_passwordchange, name="user_passwordchange"),

    #url(r'^sycco_registration/$', views.sycco_registration, name="sycco_registration"),
    #url( r'^login/$',auth_views.LoginView.as_view(template_name="useraccounts/login.html"), name="login"),
    
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
]
