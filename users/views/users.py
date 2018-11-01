
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render

from users.forms import LoginForm, PasswordChangeForm
from users.models import Sidebar, User


def login_user(request):
    """
    Login a user
    """
    next = request.GET.get('next', None)
    if request.user.is_authenticated:
        return redirect('/')

    form = LoginForm(data=request.POST or None)
    context = {
        'form': form,
    }

    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is None:
                messages.error(request, "Invalid login credentials")
                return render(request, 'users/login.html', context)
            else:
                login(request, user)
                if next:
                    return redirect(next)
                return redirect('/')
    return render(request, 'users/login.html', context)


@login_required
def user_password_change(request):
    """
    Change user password
    """
    form = PasswordChangeForm(data=request.POST or None, user=request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Password changed successfully")
            return redirect('users:user_password_change')

    context = {
        'form': form
    }
    return render(request, 'users/change_password.html', context)

@login_required
def logout_user(request):
    """
    Logout a user
    """
    logout(request)
    return redirect("users:login_user")




def change_sidebar_status(request):
    user = request.user
    if user.is_authenticated :
        sidebar_obj, new_obj = Sidebar.objects.new_or_get(request)
        sidebar_obj.is_opened = not sidebar_obj.is_opened
        sidebar_obj.save()
        request.session['sidebar_id_status'] = sidebar_obj.is_opened
        return HttpResponse('{}'.format(sidebar_obj.is_opened))
    else:
        return HttpResponse('sorry')