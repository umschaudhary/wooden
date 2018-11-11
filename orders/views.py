from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from orders.models import Order


# Create your views here.
@login_required
def order_list(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        if user.is_superuser():
            orders = Order.objects.filter(is_deleted=False)
        elif user.is_provider():
            orders = Order.objects.filter(is_deleted=False)
        else:
            messages.error(request, 'Not autorised')
            return redirect('/')
    context['orders'] = orders
    template_name = 'orders/order_list.html'
    return render(request, template_name, context)