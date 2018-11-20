from datetime import date

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, reverse

from categories.models import Category
from carts.models import Cart
from items.models import Item
from settings.models import FiscalYear
from users.models import Sidebar
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from items.models import Item as Product

# Create your views here.


def home(request):
    context = {}
    user = request.user
    active_fiscal_year = FiscalYear.get_active_fiscal_year()
    
    if user.is_authenticated :
        sidebar_obj, new_obj = Sidebar.objects.new_or_get(request)
        if user.is_superuser():
            template_name = 'pages/admin_dashboard.html'
        elif user.is_provider():
            template_name = 'pages/provider_dashboard.html'

        elif user.is_customer():
            categories = Category.objects.all_active()
            category_id = request.GET.get('category' ,'None')
            if category_id:
                try:
                    category = Category.objects.get(slug=category_id)
                except : 
                    category = None 

                if category:
                    products = category.items.all()
                else:
                    products = Product.objects.all_active()

            else:
                products = Product.objects.all_active()
 

            cart_obj, new_obj = Cart.objects.new_or_get(request)
            if cart_obj:
                items = cart_obj.cart_items.filter(is_deleted=False).count()

            context['cart'] = cart_obj
            context['item_count'] = items
            context['products'] = products
            context['categories'] = categories
            template_name = 'pages/user_dashboard.html'
        else:
            pass

# user is not authenticated down from here
    else:
        categories = Category.objects.all_active()
        category_id = request.GET.get('category')
        if category_id:
            try:
                category = Category.objects.get(slug=category_id)
            except : 
                category = None 

            if category:
                products = category.items.all()
            else:
                products = Product.objects.all_active()
        else:
            products = Product.objects.all_active()

        cart_obj, new_obj = Cart.objects.new_or_get(request)

        if cart_obj:
            items = cart_obj.cart_items.filter(is_deleted=False).count()

        context['cart'] = cart_obj
        context['item_count'] = items
        context['products'] = products
        context['categories'] = categories
        template_name = 'pages/user_dashboard.html'
    context['year'] = date.today().year
    return render(request, template_name, context)



def search_products(request):
    context = {}
    categories = Category.objects.all_active()
    query = request.GET.get('q')
    if query is not None:
        lookups = Q(name__icontains=query) | \
        Q(slug__icontains=query) | \
        Q(description__icontains=query)
        products = Product.objects.filter(lookups, is_deleted=False)
    else:
        products = Product.objects.all_active()
    context['products'] = products
    context['categories'] = categories
    return render(request, 'pages/user_dashboard.html', context)