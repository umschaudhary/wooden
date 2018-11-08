from django.shortcuts import render, redirect
from carts.models import Cart, CartItem
from users.forms import LoginForm, GuestForm
from addresses.forms import AddressForm

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
    if cart_created or cart_obj.products.count() == 0:
        return redirect('cart:cart_home')
    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_form = AddressForm()

    billing_address_id = request.session.get('billing_address_id', None)
    shipping_address_id = request.session.get('shipping_address_id', None)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if billing_profile is not None:
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()

        if request.method == "POST":
            "check that order is done"
            is_done = order_obj.check_done()
            if is_done:
                order_obj.mark_paid()
                request.session['cart_items'] = 0
                del request.session['cart_id']
                return redirect("success")

    context['order'] = order_obj
    context['form'] = login_form
    context['guest_form'] = guest_form
    context['billing_profile'] = billing_profile
    context['billing_address_form'] = billing_address_form
    context['address_form'] = address_form

    return render(request, 'carts/checkout_view.html', context)
