from items import views
from django.urls import path
app_name = 'items'

urlpatterns = [
    path('',views.category_select, name='category_select'),
    path('<int:pk>',views.item_list, name='list'),
    path('<int:pk>/create',views.item_add, name='create'),
    path('<slug:slug>', views.item_detail, name='detail'),
]
