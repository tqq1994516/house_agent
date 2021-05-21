from house_helper import views
from django.urls import path


urlpatterns = [
    path('login/', views.login.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('index/', views.index, name='index'),
    path('message/', views.message, name='message'),
    path('crm/', views.crm, name='crm'),
    path('base_info/', views.base_info, name='base_info'),
]
