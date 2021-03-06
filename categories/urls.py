from django.urls import path

from categories import views

app_name = 'categories'

urlpatterns = [
    path('', views.category_list, name='list'),
    path('create/', views.category_create, name='create'),
    path('<slug:slug>/', views.items_category, name='items_category'),
]
