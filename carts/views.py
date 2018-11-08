from django.shortcuts import render, redirect

# Create your views here.

def cart(request):
    context = {}
    template_name = 'carts/cart.html'
    return render(request, template_name, context)
