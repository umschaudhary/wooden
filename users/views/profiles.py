import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from addresses.models import Address
from billings.models import BillingProfile
from users import forms
from users.models import UserProfile


@login_required
def profile(request):
    context = {}
    try:
        profile = UserProfile.objects.get(user=request.user)
        print(profile.address_line_1)
    except UserProfile.DoesNotExist:
        profile = None

    form = forms.ProfileForm(request.POST or None, request.FILES or None, instance=profile or None)
    if request.method == 'POST':
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()
            messages.success(request, 'Profile Updated')
            return HttpResponseRedirect("")
    context['form'] = form
    context['profile'] = profile
    template_name = 'users/profile.html'
    return render(request, template_name, context)


@login_required
def load_profile(request):
    context = {}
    try:
        profile = UserProfile.objects.get(user=request.user)
        print(profile.address_line_1)
    except UserProfile.DoesNotExist:
        profile = None
    data = serializers.serialize('json', [profile, ])
    struct = json.loads(data)
    data = json.dumps(struct[0])

    return HttpResponse(data, content_type='application/json; charset=UTF-8')


def load_shipping(request):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

    if request.user.is_authenticated:
        try:
            profile = BillingProfile.objects.get(email=request.user.email)
        except BillingProfile.DoesNotExist:
            profile = None
    else:
        try:
            profile = BillingProfile.objects.get(email=request.session['guest_email'])
        except BillingProfile.DoesNotExist:
            profile = None
    try:
        address = Address.objects.get(address_type='shipping', billing_profile=profile)
    except Address.MultipleObjectsReturned:
        address = Address.objects.filter(address_type='shipping', billing_profile=profile).last()
    except Address.DoesNotExist:
        address = None

    data = serializers.serialize('json', [address, ])
    struct = json.loads(data)
    data = json.dumps(struct[0])

    return HttpResponse(data, content_type='application/json; charset=UTF-8')
