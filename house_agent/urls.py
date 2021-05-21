"""house_agent URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.staticfiles.views import serve
from django.urls import path, include, re_path
from house_helper import views

urlpatterns = [
    path('house_helper/', include('house_helper.urls')),
    re_path(r'^$', views.login.as_view(), name='login'),
    re_path(r'^login/?$', views.login.as_view(), name='login'),
    path('admin/login/', views.extend_admin_login),
    path('admin/', admin.site.urls),
    path('favicon.ico', serve, {'path': 'house_helper/img/icon/favicon.ico'}),
    re_path(r'^captcha/', include('captcha.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
