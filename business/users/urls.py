from django.urls import path,include
from . import views as user_views
from django.contrib.auth import views as auth_views
from django.conf.urls import url

urlpatterns = [
    path('signup', user_views.signup, name='signup'),
    path('profile', user_views.profile, name='profile'),
    # path('new-user', user_views.new_user, name='new_user'),
    path('signin', auth_views.LoginView.as_view(template_name='users/login.html'), name='signin'),
    path('signout', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='signout'),
    # path('edit', user_views.updateuser, name='edit'),
    # path('change_profile',user_views.profile_pic, name='change_profile'),
    path('change-password', user_views.change_password, name='change_password'),
    path('reset-password',auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='reset_password'),
    path('reset-password/done',auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_sent.html'), name='password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.PasswordResetConfirmView.as_view(template_name='users/reset_password.html'), name='password_reset_confirm'), 
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(template_name='users/Password_reset_complete.html'),name='password_reset_complete'),
]