from datetime import date

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, reverse

from settings.models import FiscalYear
from users.models import Sidebar
from items.models import Item
from carts.models import Cart


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
        else:
            pass
    else:
        products = Item.objects.all_active()
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if cart_obj:
            items = cart_obj.cart_items.filter(is_deleted=False).count()
        context['cart'] = cart_obj
        context['item_count'] = items
        template_name = 'pages/user_dashboard.html'
        context['products'] = products
    context['year'] = date.today().year
    return render(request, template_name, context)
