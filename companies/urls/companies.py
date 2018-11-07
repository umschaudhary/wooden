from django.urls import path
from companies import views

app_name = 'companies'

urlpatterns = [
    path('', views.company_list, name='list'),
    path('create/', views.company_create, name='create'),
    # path('edit/<int:pk>/', views.fiscal_year_edit, name='edit'),
    # path('change/',views.fiscal_year_change,name='change'),

]
