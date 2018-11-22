from django.urls import path

from ratings import views

urlpatterns = [
    path('<slug:slug>', views.rating_create, name='rating_create')
]
