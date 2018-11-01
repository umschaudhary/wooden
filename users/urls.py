from django.conf.urls import url

from users import views

app_name = 'users'

urlpatterns = [
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    # url(r'^register/$', views.user_register, name='user_register'),
    url(r'^send_password_reset_email/$', views.user_send_password_reset_email, name='send_password_reset_email'),
    url(r'^password_reset/$', views.user_password_reset, name='password_reset'),
    url(r'^change_password/$', views.user_password_change, name='user_password_change'),
    url(r'^profile/$', views.user_profile_edit, name="profile_edit"),
    url(r'^ward_user_register/(?P<pk>\d+)/$', views.ward_user_register, name="ward_user_register"),
    url(r'^ward_users/(?P<pk>\d+)/$', views.ward_users, name="ward_users"),
    url(r'^change_sidebar_status/$', views.change_sidebar_status, name="sidebar_status"),
     
    # url(r'^confirm_email/$', views.user_email_confirm, name='email_confirm'),
]
