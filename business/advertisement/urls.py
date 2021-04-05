from django.urls import path

from .views import (
 CreateAdView, 
 EditAdView, 
 ListAdView, 
 DeleteAdView , 
 search,
 AdClickView,
)

urlpatterns = [
    path('create/',CreateAdView.as_view(), name='create_ad'),
    path('editad/<int:pk>/',EditAdView.as_view(), name='edit_ad'),
    path('showad/', ListAdView.as_view(), name='show_ad'),
    path('deletead/<int:pk>/', DeleteAdView.as_view(), name='delete_ad'),
    path('searchad/',search,name='search_ad'),
    path('clickad/<int:pk>/', AdClickView.as_view(), name = 'click_ad')
]