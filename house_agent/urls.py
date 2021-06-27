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
from django.urls import path, include, re_path
from house_helper import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'menus', views.MenuViewSet)
router.register(r'baseInfo', views.BaseInfoViewSet)
router.register(r'callLog', views.CallLogViewSet)
router.register(r'tagType', views.TagTypeViewSet)
router.register(r'tag', views.TagViewSet)
router.register(r'tagRule', views.TagRuleViewSet)
router.register(r'houseInfo', views.HouseInfoViewSet)
router.register(r'tagRuleRelation', views.TagRuleRelationViewSet)
router.register(r'tagRelation', views.TagRelationViewSet)

urlpatterns = [
    path('house_helper/', include('house_helper.urls')),
    re_path(r'^login/?$', views.Login.as_view(), name='login'),
    re_path(r'^logout/?$', views.Logout.as_view(), name='logout'),
    re_path(r'^register/?$', views.Register.as_view(), name='register'),
    re_path(r'^administrativeDivision/?$', views.administrativeDivision.as_view(), name='administrativeDivision'),
    path('admin/', admin.site.urls),
    re_path(r'^captcha/', include('captcha.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(router.urls)),
]
