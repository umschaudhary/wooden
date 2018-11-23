from  django.urls import path

from data_analysis.api import views

urlpatterns = [
    path('orders/', views.char_data),
    path('order_list/', views.cartdata),
    path('customer_data/', views.customer_count),
]
