from django.urls import path, include
from rest.views import (
    TestView, 
    LogDataView, 
    UniqueIDAPIView, 
    ImageAPIView,
    CategoryAPIView,
    CategoryNewsAPIView
)
from django.conf.urls import url
# from rest_framework.authtoken.views import obtain_auth_token 

urlpatterns = [
    # path('api-auth/', include('rest_framework.urls')),
    path('allnews/',TestView.as_view(),name='newsapi'),
    path('allcategories/',CategoryAPIView.as_view(),name='categoryapi'),
    path('getimage/<int:pk>/',ImageAPIView.as_view(),name='imageapi'),
    path('catnews/<slug:slug>/',CategoryNewsAPIView.as_view(),name='catnewsapi'),
    # path('token/', obtain_auth_token, name = 'obtain-token'),
    # path('rest-auth/', include('rest_auth.urls')),
    path('log-data/',LogDataView.as_view(), name='logdata'),
    path('random-id/',UniqueIDAPIView.as_view(),name='userID')
]