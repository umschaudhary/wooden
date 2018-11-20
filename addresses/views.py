from .forms import AddressForm
from django.shortcuts import redirect, render
from django.utils.http import is_safe_url

from addresses.models import Address
from billings.models import BillingProfile
from django.contrib import messages


def shipping_address(request):
    context = {}
    shipping_address_id = request.session.get('shipping_address_id', None)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    try:
        if request.user.is_authenticated:
            address_instance = Address.objects.get(is_deleted=False,address_type='shipping',billing_profile=billing_profile)
        else:
            address_instance = Address.objects.get(is_deleted=False,address_type='shipping',billing_profile=billing_profile, id=shipping_address_id)

    except Address.DoesNotExist:
        address_instance = None
    except Address.MultipleObjectsReturned:
        if request.user.is_authenticated:
            qs = Address.objects.filter(is_deleted=False,address_type='shipping',billing_profile=billing_profile)
            address_instance = qs.last()
        else:
            qs = Address.objects.filter(is_deleted=False,address_type='shipping',billing_profile=billing_profile, id=shipping_address_id)
            address_instance = qs.last()


    form = AddressForm(request.POST or None, instance=address_instance or None)
        
    if billing_profile is not None:
        if request.method == 'POST':
            if form.is_valid():
                instance = form.save(commit=False)
                instance.address_type = 'shipping'
                instance.billing_profile = billing_profile
                instance.save()
                request.session["shipping_address_id"] = instance.id
                messages.success(request, 'Shipping Address has been Added')
                return redirect('addresses:billing_address')
    else:
        print("Error here")
        return redirect("carts:checkout")

    context['address_form'] = form
    return render(request, 'addresses/shipping_address.html', context)

def billing_address(request):
    context = {}
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    billing_address_id = request.session.get('billing_address_id', None)

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)


    try:
        billing_address_instance = Address.objects.get(is_deleted=False, address_type='billing', billing_profile=billing_profile,  id=billing_address_id)
    except Address.MultipleObjectsReturned:
        qs = Address.objects.filter(is_deleted=False,address_type='billing',billing_profile=billing_profile, id=billing_address_id)
        billing_address_instance = qs.last()
    except Address.DoesNotExist:
        billing_address_instance = None
    form = AddressForm(request.POST or None, instance=billing_address_instance or None)

    if billing_profile is not None:
        if request.method == 'POST':
            if form.is_valid():
                data = form.save(commit=False)
                data.address_type = 'billing'
                data.billing_profile = billing_profile
                data.save()
                request.session["billing_address_id"] = data.id
                messages.success(request, 'Billing Address has been Added')
                return redirect("carts:checkout")
    else:
        print("Error here")
        return redirect("carts:checkout")

    context['billing_address_form'] = form
    return render(request, 'addresses/billing_address.html', context)
