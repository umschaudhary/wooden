from django.shortcuts import redirect, render
from django.urls import reverse

from addresses.forms import AddressForm
from addresses.models import Address
from billings.models import BillingProfile
from carts.models import Cart, CartItem
from orders.models import Order
from users.forms import GuestForm, LoginForm


# Create your views here.

def cart(request):
    context = {}
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    context['cart'] = cart_obj
    if cart_obj:
        cart_items = cart_obj.cart_items.all()
        context['objects'] = cart_items

    template_name = 'carts/cart.html'
    
    return render(request, template_name, context)


def checkout(request):
    context = {}
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    billing_address_id = request.session.get('billing_address_id', None)
    shipping_address_id = request.session.get('shipping_address_id', None)

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

    order_obj = None
    if cart_created or cart_obj.cart_items.count() == 0:
        return redirect('carts:cart')

    login_form = LoginForm()
    guest_form = GuestForm()

    try:
        address_instance = Address.objects.get(is_deleted=False,address_type='shipping',billing_profile=billing_profile)
    
    except Address.DoesNotExist:
        address_instance = None
    except Address.MultipleObjectsReturned:
        qs = Address.objects.filter(is_deleted=False,address_type='shipping',billing_profile=billing_profile)
        address_instance = qs.first()

    address_form = AddressForm(instance=address_instance)

    try:
        billing_address_instance = Address.objects.get(is_deleted=False,address_type='billing',billing_profile=billing_profile)
    except Address.DoesNotExist:
        billing_address_instance = None
        
    except Address.MultipleObjectsReturned:
        qs = Address.objects.filter(is_deleted=False,address_type='billing',billing_profile=billing_profile)
        billing_address_instance = qs.first()
    billing_address_form = AddressForm(instance=billing_address_instance)

    

    if billing_profile is not None:
        print('billing exist')
        order_obj, new_obj = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            print(shipping_address_id)
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            print(billing_address_id)
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()

        if request.method == "POST":
            is_done = order_obj.check_done()
            if is_done:
                del request.session['cart_id']
                return redirect("success")

    context['order'] = order_obj
    context['form'] = login_form
    context['guest_form'] = guest_form
    context['billing_profile'] = billing_profile
    context['billing_address_form'] = billing_address_form
    context['address_form'] = address_form

    return render(request, 'carts/checkout.html', context)


def success(request):
    context = {}

    cart_obj, cart_created = Cart.objects.new_or_get(request)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.cart_items.count() == 0:
        return redirect('carts:cart')

    try:
        address_instance = Address.objects.get(is_deleted=False,address_type='shipping',billing_profile=billing_profile)
    
    except Address.DoesNotExist:
        address_instance = None
    except Address.MultipleObjectsReturned:
        qs = Address.objects.filter(is_deleted=False,address_type='shipping',billing_profile=billing_profile)
        address_instance = qs.first()

    try:
        billing_address_instance = Address.objects.get(is_deleted=False,address_type='billing',billing_profile=billing_profile)
    except Address.DoesNotExist:
        billing_address_instance = None
        
    except Address.MultipleObjectsReturned:
        qs = Address.objects.filter(is_deleted=False,address_type='billing',billing_profile=billing_profile)
        billing_address_instance = qs.first()


    if billing_profile is not None:
        print('billing exist')
        order_obj, new_obj = Order.objects.new_or_get(billing_profile, cart_obj)
        if address_instance:
            print(billing_address_instance)
            order_obj.shipping_address = Address.objects.get(id=address_instance.id)
        if billing_address_instance:
            print(billing_address_instance)
            order_obj.billing_address = Address.objects.get(id=billing_address_instance.id)
        if address_instance or billing_address_instance:
            order_obj.save()

    context['order'] = order_obj
    template_name = 'success.html'
    return render(request, template_name, context)