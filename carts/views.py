from django.shortcuts import render, redirect
from carts.models import Cart, CartItem
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
