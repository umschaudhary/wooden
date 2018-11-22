from django.urls import path

from data_analysis import views

app_name = 'data_analysis'
urlpatterns = [
    path('orders/', views.orders, name='orders')
]
