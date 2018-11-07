from django.urls import path
from companies import views

app_name = 'company_users'

urlpatterns = [
    path('<int:pk>', views.company_users, name='list'),
    path('<int:pk>/create/', views.company_user_create, name='create'),
    path('<int:pk>/change_status/', views.company_user_change_status, name='change_status'),

]
