"""business URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include
from home import views as homeview
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin987/', admin.site.urls),
    path("",homeview.index, name='index'),
    path("search",homeview.search, name='search'),
    path('users/', include('users.urls')),
    path('news/', include('news.urls')),
    path('ad/', include('advertisement.urls')),
    path('test/', include('testing.urls')),
    path('drf/', include('rest.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
