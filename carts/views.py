from django.shortcuts import redirect, render 
from django.urls import reverse

from addresses.forms import AddressForm
from addresses.models import Address
from billings.models import BillingProfile
from carts.models import Cart, CartItem
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
    order_obj = None
    if cart_created or cart_obj.cart_items.count() == 0:
        return redirect('carts:cart')
    login_form = LoginForm()
    guest_form = GuestForm()
    
    address_form = AddressForm()
    billing_address_form = AddressForm()

    billing_address_id = request.session.get('billing_address_id', None)
    shipping_address_id = request.session.get('shipping_address_id', None)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if billing_profile is not None:
        if request.method == "POST":
            if address_form.is_valid():
                address_form.save()
            return redirect("/")

    context['order'] = order_obj
    context['form'] = login_form
    context['guest_form'] = guest_form
    context['billing_profile'] = billing_profile
    context['billing_address_form'] = billing_address_form
    context['address_form'] = address_form

    return render(request, 'carts/checkout.html', context)
