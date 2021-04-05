from django.urls import path,include
from . import views 
from django.contrib.auth import views as auth_views
from django.conf.urls import url

urlpatterns = [
    path('post', views.post, name='post'),
    # path('all', views.all_news, name='all_news'),
   
]