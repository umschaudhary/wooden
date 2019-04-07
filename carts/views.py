from django.contrib import messages
from django.shortcuts import redirect, render
from addresses.models import Address
from billings.models import BillingProfile
from carts.models import Cart, CartItem
from orders.models import Order, OrderItem
from users.forms import GuestForm, LoginForm


# Create your views here.

def cart(request):
    context = {}
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    context['cart'] = cart_obj
    if cart_obj:
        cart_items = cart_obj.cart_items.all()
        request.session['item_count'] = cart_items.count()
        context['objects'] = cart_items
        total = 0
        for item in cart_items:
            total += item.total
        cart_obj.total = total
        cart_obj.save()

    template_name = 'carts/cart.html'
    return render(request, template_name, context)


def checkout(request):
    context = {}
    print('url = ',request.build_absolute_uri)
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    billing_address_id = request.session.get('billing_address_id', None)
    shipping_address_id = request.session.get('shipping_address_id', None)
    
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

    order_obj = None
    if cart_created or cart_obj.cart_items.count() == 0:
        return redirect('/')

    login_form = LoginForm()
    guest_form = GuestForm()

    if billing_profile : 
        if not shipping_address_id :
            return redirect('addresses:shipping_address')
        if not billing_address_id:
            return redirect('addresses:billing_address')
        context['shipping_address'] = Address.objects.get(id=shipping_address_id, billing_profile=billing_profile)
        context['billing_address'] = Address.objects.get(id=billing_address_id,  billing_profile=billing_profile)

    if request.method == "POST":
        if billing_profile is not None:
            print('billing exist')
            order_obj, new_obj = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            print(shipping_address_id)
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
        if billing_address_id:
            print(billing_address_id)
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
        if billing_address_id or shipping_address_id:
            order_obj.save()

            order_item = OrderItem()
            for item in cart_obj.cart_items.all():
                order_item = OrderItem()
                order_item.order = order_obj
                order_item.item = item.item
                order_item.quantity = item.quantity
                order_item.total = item.total
                order_item.save()
                
            cart_obj.cart_items.all().delete()
            del request.session['item_count']
            return redirect("success")

    context['order'] = order_obj
    context['form'] = login_form
    context['guest_form'] = guest_form
    context['cart'] = cart_obj
    context['billing_profile'] = billing_profile

    return render(request, 'carts/checkout.html', context)


def success(request):
    context = {}
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

    if billing_profile is not None:
        print('billing exist')
        order_obj, new_obj = Order.objects.new_or_get(billing_profile, cart_obj)
    context['order'] = order_obj
    template_name = 'success.html'
    return render(request, template_name, context)


def item_remove_cart(request,pk):
    context= {}
    try:
        cart_item = CartItem.objects.get(pk=pk)
    except CartItem.DoesNotExist:
        cart_item = None
    if cart_item :
        cart_item.delete()
        item_stock = cart_item.item.stock_record
        item_stock.quantity += cart_item.quantity
        item_stock.save()
        messages.success(request, 'Item Removed form cart')
    
    return redirect('carts:cart')


def item_quantity_minus(request, pk):
    context = {}
    try:
        cart_item = CartItem.objects.get(pk=pk)
    except CartItem.DoesNotExist:
        cart_item = None
    if cart_item :
        item_stock = cart_item.item.stock_record
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            item_stock.quantity += 1
            item_stock.save()

    return redirect('carts:cart')

def item_quantity_plus(request, pk):
    context = {}
    try:
        cart_item = CartItem.objects.get(pk=pk)
    except CartItem.DoesNotExist:
        cart_item = None
    if cart_item:
        item_stock = cart_item.item.stock_record
        
        if not item_stock.quantity == 0:
            cart_item.quantity += 1
            cart_item.save()
            item_stock.quantity -= 1
            item_stock.save()
        else:
            messages.error(request, 'Out of stock')

    return redirect('carts:cart')