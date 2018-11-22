from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from categories.models import Category
from refunds import forms
from refunds.models import RefundPolicy, RefundRequest
from users.decorators import provider_required


# Create your views here.

@login_required
@provider_required
def refund_policy_create(request, slug=None):
    context = {}

    try:
        category = Category.objects.get(slug=slug, is_deleted=False)
    except Category.DoesNotExist:
        category = None
    except Category.MultipleObjectsReturned:
        category = Category.objects.filter(slug=slug, is_deleted=False).last()

    provider = request.user.company_admin.company
    try:
        policy = RefundPolicy.objects.filter(category=category, provider=provider).last()
    except RefundPolicy.DoesNotExist:
        policy = None

    form = forms.RefundPolicyForm(request.POST or None, instance=policy or None)
    if category:
        if request.user.is_authenticated and request.user.is_provider():
            if request.method == 'POST':
                if form.is_valid():
                    data = form.save(commit=False)
                    data.provider = request.user.company_admin.company
                    data.category = category
                    data.save()
                    return redirect('items:category_select')

    context['form'] = form
    context['category'] = category
    template_name = 'refunds/refund_policy_create.html'
    return render(request, template_name, context)


@login_required
@provider_required
def refund_request_list(request):
    context = {}
    provider = request.user.company_admin.company
    refunds = RefundRequest.objects.filter(is_deleted=False, order_item__item__provider=provider)

    template_name = 'refunds/refund_request_list.html'
    context['refunds'] = refunds
    return render(request, template_name, context)
