from django.urls import path
from carts import views
app_name = 'carts'

urlpatterns = [
    path('', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('item_remove_cart/<int:pk>/', views.item_remove_cart, name='item_remove_cart'),
    path('item_quantity_minus/<int:pk>/', views.item_quantity_minus, name='item_quantity_minus'),
    path('item_quantity_plus/<int:pk>/', views.item_quantity_plus ,name='item_quantity_plus'),
    
    

]
