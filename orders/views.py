from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect

from orders import forms
from orders.models import Order, OrderItem, ORDER_STATUS_CHOICES
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
            orders = Order.objects.filter(is_deleted=False,
                                          order_items__item__provider=user.company_admin.company).distinct()
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
    except Order.MultipleObjectsReturned:
        order = Order.objects.filte(pk=pk, is_deleted=False).last()

    except Order.DoesNotExist:
        order = None

    if order:
        items = order.order_items.filter(is_deleted=False, item__provider=user.company_admin.company)
        if items:
            status = all(x.status == items[0].status for x in items)
            print('yes ', status)
            if status:
                if not order.status == items[0].status:
                    order.status = items[0].status
                    order.save()

        context['objects'] = items
        context['order'] = order
        total_count = items.aggregate(Sum('total'))
        order_total = total_count['total__sum']
        context['order_total'] = order_total

    context['statuses'] = ['created', 'paid', 'refunded', 'delivered', 'processed']
    template_name = 'orders/order_items.html'
    return render(request, template_name, context)


@login_required
@provider_required
def item_status_update(request, pk):
    context = {}
    try:
        item = OrderItem.objects.get(pk=pk)
    except OrderItem.DoesNotExist:
        item = None
    form = forms.OrderItemStatusForm(request.POST or None, instance=item)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request,'Status changed')
            return redirect("orders:order_items", item.order.pk)

    context['form'] = form
    context['item'] =item
    template_name = 'orders/item_status_update.html'
    return render(request, template_name, context)
