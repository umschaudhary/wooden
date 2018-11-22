from datetime import date

from django.db.models import Q
from django.shortcuts import render

from carts.models import Cart, CartItem
from categories.models import Category
from items.models import Item as Product
from orders.models import Order
from refunds.models import RefundRequest
from settings.models import FiscalYear
from users.models import Sidebar


# Create your views here.


def home(request):
    context = {}
    user = request.user
    active_fiscal_year = FiscalYear.get_active_fiscal_year()

    if user.is_authenticated:
        sidebar_obj, new_obj = Sidebar.objects.new_or_get(request)
        if user.is_superuser():
            template_name = 'pages/admin_dashboard.html'
        elif user.is_provider():
            provider = request.user.company_admin.company
            orders = Order.objects.filter(is_deleted=False,
                                          order_items__item__provider=provider).order_by("-updated_at").distinct()[:5]
            requests = RefundRequest.objects.filter(is_deleted=False,
                                                    order_item__item__provider=provider)[:5]

            context['orders'] = orders
            context['requests'] = requests
            context['provider'] = provider
            template_name = 'pages/provider_dashboard.html'

        elif user.is_customer():
            print(request.user.id)
            cart_id = request.session.get('cart_id', None)
            print(cart_id)
            try:
                cart = Cart.objects.get(id=cart_id, user=None)
            except Cart.DoesNotExist:
                cart = None

            if cart:
                items = cart.cart_items.all()
            else:
                items = None

            try:
                cart_obj = Cart.objects.get(user_id=request.user.id)
                if cart and items.count() > 0:
                    for item in items:
                        try:
                            item_in_cart = CartItem.objects.get(cart=cart_obj, item=item.item)
                        except CartItem.DoesNotExist:
                            item_in_cart = None

                        if item_in_cart:
                            item_in_cart.quantity += item.quantity
                            item_in_cart.save()
                        else:
                            cart_item = CartItem()
                            cart_item.cart = cart_obj
                            cart_item.item = item.item
                            cart_item.total = item.total
                            cart_item.quantity = item.quantity
                            cart_item.save()
                            items.delete()
                            cart.delete()

                request.session['cart_id'] = cart_obj.id
                request.session['item_count'] = cart_obj.cart_items.all().count()
            except Cart.MultipleObjectsReturned:
                qs = Cart.objects.filter(user_id=request.user.id)
                if qs:
                    cart_obj = qs.last()
                    if cart and items.count() > 0:
                        for item in items:
                            try:
                                item_in_cart = CartItem.objects.get(cart=cart_obj, item=item.item)
                            except CartItem.DoesNotExist:
                                item_in_cart = None
                            if item_in_cart:
                                item_in_cart.quantity += item.quantity
                                item_in_cart.save()
                            else:
                                cart_item = CartItem()
                                cart_item.cart = cart_obj
                                cart_item.item = item.item
                                cart_item.total = item.total
                                cart_item.quantity = item.quantity
                                cart_item.save()
                                items.delete()
                                cart.delete()
                    request.session['cart_id'] = cart_obj.id
                    request.session['item_count'] = cart_obj.cart_items.all().count()
            except Cart.DoesNotExist:
                cart_obj, new_obj = Cart.objects.new_or_get(request)
            categories = Category.objects.all_active()
            category_id = request.GET.get('category', 'None')
            if category_id:
                try:
                    category = Category.objects.get(slug=category_id)
                except:
                    category = None

                if category:
                    products = category.items.all()
                else:
                    products = Product.objects.all_active()
            else:
                products = Product.objects.all_active()
            context['cart'] = cart_obj
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
            except:
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
