"""b2e URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from home.views import home as home_page
from home.views import create as url_create
from home.views import result as url_result
from home.views import url_handler

urlpatterns = [
    path('', home_page, name='home_page'),
    path('url/create', url_create, name='url_create'),
    re_path(r'^url/result/(?P<url_hash>[0-9A-Za-z]{1,12})/$', url_result, name='url_result'),
    re_path(r'^go/(?P<url_hash>[0-9A-Za-z]{1,12})/$', url_handler, name='url_handler'),
    path('admin/', admin.site.urls),
]
