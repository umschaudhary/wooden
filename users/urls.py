from django.conf.urls import url

from users import views

app_name = 'users'

urlpatterns = [
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^change_password/$', views.user_password_change, name='user_password_change'),
  
     
    # url(r'^confirm_email/$', views.user_email_confirm, name='email_confirm'),
]
