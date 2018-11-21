from django.contrib.auth.decorators import login_required
from django.db.models import Sum
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
            context['orders'] = orders
        elif user.is_provider():
            orders = Order.objects.filter(is_deleted=False, order_items__item__provider=user.company_admin.company).distinct()
            context['orders'] = orders

        else:
            messages.error(request, 'Not authorised')
            return redirect('/')



    template_name = 'orders/order_list.html'
    return render(request, template_name, context)



@login_required
@provider_required
def order_items(request, pk):
    context = {}
    user = request.user
    try:
        order = Order.objects.get(pk=pk, is_deleted=False)
        if order:
            items = order.order_items.filter(is_deleted=False, item__provider=user.company_admin.company)
            context['objects'] = items
            context['order'] = order
            total_count = items.aggregate(Sum('total'))
            order_total = total_count['total__sum']
            context['order_total'] = order_total
    except Order.MultipleObjectsReturned:
        qs = Order.objects.filte(pk=pk, is_deleted=False)
        if qs:
            order = qs.last()
            if order:
                items = order.order_items.filter(is_deleted=False, item__provider=user.company_admin.company)
                total_count = items.aggregate(Sum('total'))
                order_total = total_count['total__sum']
                context['order_total'] = order_total
                context['objects'] = items
                context['order'] = order
    except Order.DoesNotExist:
        order = None


    template_name = 'orders/order_items.html'
    return render(request, template_name, context)
