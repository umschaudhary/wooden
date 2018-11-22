from django.urls import path

from orders import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='list'),
    path('<int:pk>/items/', views.order_items, name='order_items'),
    path('<int:pk>/update/', views.item_status_update, name='item_status_update'),
    path('history', views.order_history, name='order_history'),
    path('<int:pk>/order_items', views.order_item_customer, name='order_item_customer'),
    path('<int:pk>/order_cancel_item', views.order_cancel_item, name='order_cancel_item'),
    path('<int:pk>/refund_request_create', views.order_refund_request_create, name='refund_request_create')
]
