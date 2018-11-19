
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.utils.http import is_safe_url
from users import forms 
from users.models import  User, GENDER_TYPES , UserProfile
from django.http import JsonResponse
import json
from django.core import serializers

@login_required
def profile(request):
    context = {}
    try: 
        profile = UserProfile.objects.get(user=request.user)
        print(profile.address_line_1)
    except UserProfile.DoesNotExist:
        profile = None
    
    form = forms.ProfileForm(request.POST or None,request.FILES or None ,instance=profile or None)
    if request.method == 'POST':
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()
            messages.success(request, 'Profile created')
            return redirect('/')
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
    data = serializers.serialize('json', [profile,])
    struct = json.loads(data)
    data = json.dumps(struct[0])
    
    return HttpResponse(data, content_type='application/json; charset=UTF-8')
