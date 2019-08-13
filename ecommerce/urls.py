"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from carts.views import success
from pages import views
from users.views import guest_register_view, register_page, login_admin

urlpatterns = [
                  path('', views.home, name='home'),
                  path('admin/', admin.site.urls),
                  path('addresses/', include('addresses.urls')),
                  path('users/', include('users.urls')),
                  path('cart/', include('carts.urls')),
                  path('companies/', include('companies.urls.companies')),
                  path('company_users/', include('companies.urls.company_users')),
                  path('comments/', include('comments.urls')),
                  path('categories/', include('categories.urls')),
                  path('data-analysis/', include('data_analysis.urls')),
                  path('fiscal-years/', include('settings.urls.fiscal_years')),
                  path('guest_register/', guest_register_view,
                       name='guest_register'),
                  path('items/', include('items.urls')),
                  path('login_admin/', login_admin, name='login_admin'),
                  path('orders/', include('orders.urls')),
                  path('ratings/', include('ratings.urls')),
                  path('refunds/', include('refunds.urls')),
                  path('register/', register_page, name='register'),
                  path('success/', success, name='success'),
                  path('search_products/', views.search_products,
                       name='search_products'),
                  path('api/v1/data/', include('data_analysis.api.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)