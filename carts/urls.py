from django.urls import path
from carts import views
app_name = 'carts'

urlpatterns = [
    path('', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
]
