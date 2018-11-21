from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from orders.models import Order
from users.decorators import provider_required


@login_required
@provider_required 
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



@login_required
@provider_required
def order_items(request, pk):
    context = {}
    try:
        order = Order.objects.get(pk = pk, is_deleted=False)
    except Order.MultipleObjectsReturned:
        qs = Order.objects.filte(pk=pk, is_deleted=False)
        if qs:
            order = qs.last()
    except Order.DoesNotExist:
        messages.error(request, 'order Not Found')
        return redirect('orders:list')
    if order:
        items = order.order_items.all()
    context['objects'] = items
    context['order'] = order
    template_name = 'orders/order_items.html'
    
    return render(request, template_name, context)
