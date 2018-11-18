
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.utils.http import is_safe_url
from users import forms 
from users.models import  User, GENDER_TYPES , UserProfile


@login_required
def profile(request):
    context = {}
    try: 
        profile = UserProfile.objects.get(user=request.user)
        print('ayo hai pro')
    except UserProfile.DoesNotExist:
        profile = None
    
    form = forms.ProfileForm(request.POST or None,request.FILES ,instance=profile)
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

