from django.urls import path

from addresses import views
app_name = 'addresses'

urlpatterns = [
    path('shipping_address',views.shipping_address, name='shipping_address'),
    path('billing_address',views.billing_address, name='billing_address')
]