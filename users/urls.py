
from users import views
from django.urls import path 
app_name = 'users'

urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('change_password/', views.user_password_change, name='user_password_change'),
    path('change_sidebar_status/', views.change_sidebar_status, name="sidebar_status"),
  
     
    # url(r'^confirm_email/$', views.user_email_confirm, name='email_confirm'),
]
