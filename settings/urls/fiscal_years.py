from django.urls import path
from settings import views

app_name = 'fiscal_years'

urlpatterns = [
    path('', views.fiscal_year_list, name='list'),
    path('create/', views.fiscal_year_create, name='create'),
    path('edit/<int:pk>/', views.fiscal_year_edit, name='edit'),
    path('change/',views.fiscal_year_change,name='change'),

]
