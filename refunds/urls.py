from django.urls import path

from refunds import views

app_name = 'refunds'

urlpatterns = [
    path('request_list/', views.refund_request_list, name='refund_request_list'),
    path('<slug:slug>/', views.refund_policy_create, name='create'),

]
