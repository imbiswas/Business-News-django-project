from django.urls import path, include
from . import views 
from django.contrib.auth import views as auth_views
from django.conf.urls import url

urlpatterns = [
    path('add', views.add_news, name='add_news'),
    path('add_headline', views.add_headline_news, name='add_headline'),
    path('all', views.all_news, name='all_news'),
    path('category', views.category, name='category'),
    path('nsearch',views.search, name ='nsearch'),
    path('<slug:slug>/update',views.NewsUpdate.as_view(),name ='news_update'),
    path('<slug:slug>/delete',views.NewsDelete.as_view(),name ='news_delete'),
    path('deleteheadline/<int:pk>/', views.HeadlineDelete.as_view(), name='headline_delete'),
    path('category/<str:category>', views.this_category, name='from_category'),
    # path('<slug:slug>', views.show_one_item, name="show_one_item"),
    path('showall', views.NewsListView.as_view(), name="show_all"),
    path('showall_headlines', views.HeadlineListView.as_view(), name="show_all_headlines"),
    path('<slug:slug>', views.NewsDetailView.as_view(), name="show_one_item"),
   
]