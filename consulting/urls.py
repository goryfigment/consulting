"""consulting URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from consulting.controllers import site, account_handler, database

urlpatterns = [
    url(r'^$', site.home, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^register/$', site.register, name='register_page'),
    url(r'^login/$', site.login, name='login_page'),
    url(r'^forgot_password/$', site.forgot_password, name='forgot_password'),
    url(r'^dashboard/$', site.dashboard, name='dashboard'),

    # Account Handler
    url(r'^account/register/$', account_handler.register, name='register'),
    url(r'^account/login/$', account_handler.user_login, name='login'),
    url(r'^account/reset_password/$', account_handler.reset_password, name='reset_password'),
    url(r'^account/change_password/$', account_handler.change_password, name='change_password'),
    url(r'^logout/$', account_handler.user_logout, name='logout'),

    # Database
    url(r'^database/table_columns/$', database.get_table_columns, name='table_columns'),
    url(r'^database/relationship_map/$', database.get_relationships, name='relationship_map'),
    url(r'^database/create_query/$', database.create_query, name='create_query'),
    url(r'^database/get_query/$', database.get_query, name='get_query'),
]
