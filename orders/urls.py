from django.urls import path
from orders import views

app_name = 'orders'

urlpatterns = [
    path('',views.order_list, name='list'),
    path('<int:pk>/items/',views.order_items, name='order_items'),
]
