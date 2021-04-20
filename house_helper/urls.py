from house_helper import views
from django.urls import path, re_path


urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('index/', views.index, name='index')
]
