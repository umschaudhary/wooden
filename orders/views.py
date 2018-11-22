from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from billings.models import BillingProfile
from orders import forms
from orders.models import Order, OrderItem
from refunds.forms import RefundRequestForm
from refunds.models import RefundRequest
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
        items = order.order_items.filter(
            is_deleted=False, item__provider=user.company_admin.company)
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

    context['statuses'] = ['created', 'paid',
                           'refunded', 'delivered', 'processed']
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
            messages.success(request, 'Status changed')
            return redirect("orders:order_items", item.order.pk)

    context['form'] = form
    context['item'] = item
    template_name = 'orders/item_status_update.html'
    return render(request, template_name, context)


@login_required
def order_history(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        if user.is_customer():
            orders = Order.objects.filter(
                is_deleted=False, billing_profile__user=user)
            context['orders'] = orders
    template_name = 'orders/order_history.html'
    return render(request, template_name, context)


@login_required
def order_item_customer(request, pk):
    context = {}
    user = request.user
    if user.is_authenticated:
        if user.is_customer():
            try:
                order = Order.objects.get(pk=pk, billing_profile__user=user)
            except Order.DoesNotExist:
                order = None

            if order:
                items = order.order_items.all()
                total_count = items.aggregate(Sum('total'))
                order_total = total_count['total__sum']
                context['order_total'] = order_total
                context['order'] = order
                context['items'] = items
    template_name = 'orders/order_item_customer.html'
    return render(request, template_name, context)


@login_required
def order_cancel_item(request, pk):
    context = {}
    try:
        item = OrderItem.objects.get(pk=pk)
    except OrderItem.DoesNotExist:
        item = None
    if request.method == 'POST':
        item.status = 'cancelled'
        item.save()
        return redirect('orders:order_item_customer', item.order.pk)

    context['item'] = item
    context['next'] = reverse('orders:order_item_customer', kwargs={'pk': item.order.pk})
    template_name = 'snippets/cancel_item.html'
    return render(request, template_name, context)


@login_required
def order_refund_request_create(request, pk):
    context = {}
    try:
        item = OrderItem.objects.get(pk=pk)
    except OrderItem.DoesNotExist:
        item = None
    try:
        refund = RefundRequest.objects.get(billing_profile__user=request.user, order_item=item)

        if refund:
            if refund.quantity == item.quantity:
                context['is_requested'] = True
    except RefundRequest.MultipleObjectsReturned:
        refund = RefundRequest.objects.filter(billing_profile__user=request.user, order_item=item).last()
        if refund.quantity == item.quantity:
            context['is_requested'] = True
    except RefundRequest.DoesNotExist:
        refund = None
        context['is_requested'] = False

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

    form = RefundRequestForm(request.POST or None, instance=refund or None)
    if request.method == 'POST':
        if form.is_valid():
            data = form.save(commit=False)
            quantity = form.cleaned_data['quantity']
            if quantity <= item.quantity:
                data.order_item = item
                data.billing_profile = billing_profile
                data.quantity = quantity
                data.save()
                messages.success(request, ' Refund Request Successfully Submitted')
                return redirect("orders:order_item_customer", item.order.pk)
            else:
                messages.error(request, 'Quantity should not exceed order item quantity')
                return HttpResponseRedirect("")

    context['refund'] = refund
    context['form'] = form
    template_name = 'orders/order_refund_request_create.html'
    return render(request, template_name, context)
