from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('change_password/', views.user_password_change, name='user_password_change'),
    path('change_sidebar_status/', views.change_sidebar_status, name="sidebar_status"),
    path('register/',views.register_page,name='register'),
    path('profile/', views.profile, name='profile'),
    path('load_profile/',views.load_profile, name='load_profile'),
    path('load_shipping/',views.load_shipping, name='load_shipping'),
  
     
    # url(r'^confirm_email/$', views.user_email_confirm, name='email_confirm'),
]
