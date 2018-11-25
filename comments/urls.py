from django.urls import path
from comments import views

urlpatterns = [
    path('create/<slug:slug>',views.comment_create, name='comment_create')

]