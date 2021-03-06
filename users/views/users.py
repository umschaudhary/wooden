from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.http import is_safe_url

from users.forms import GuestForm, LoginForm, PasswordChangeForm, \
    RegisterForm
from users.models import GuestEmail, Sidebar, USER_ROLES


def login_user(request):
    """
    Login a user
    """
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
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
                if user.is_active:
                    if user.is_customer():
                        login(request, user)
                        try:
                            del request.session['guest_email_id']
                        except:
                            pass
                        if is_safe_url(redirect_path, request.get_host()):
                            return redirect(redirect_path)
                        return redirect('/')
                    else:
                        messages.error(request, 'Login through admin Panel')
                        return redirect('login_admin')
                else:
                    messages.error(request, 'Inactive Account, Contact Admin')
    return render(request, 'users/login.html', context)

3
def login_admin(request):
    """
    Login a user
    """
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
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
                if user.is_active:
                    login(request, user)
                    try:
                        del request.session['guest_email_id']
                    except:
                        pass
                    if is_safe_url(redirect_path, request.get_host()):
                        return redirect(redirect_path)
                    return redirect('/')
                else:
                    messages.error(request, 'Inactive Account, Contact Admin')

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


def guest_register_view(request):
    form = GuestForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email = form.cleaned_data.get("email")
        try:
            new_guest_email = GuestEmail.objects.get(email=email)

        except GuestEmail.MultipleObjectsReturned:
            qs = GuestEmail.objects.create(email=email)
            if qs:
                new_guest_email = qs.last()
        except:
            new_guest_email = GuestEmail.objects.create(email=email)

        request.session['guest_email_id'] = new_guest_email.id
        request.session['guest_email'] = email
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("carts:checkout")
    return redirect("carts:checkout")


def register_page(request):
    next = request.GET.get('next', None)
    if request.user.is_authenticated:
        return redirect('/')
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        data = form.save(commit=False)
        data.role = USER_ROLES.customer
        data.save()
        messages.info(request, "Thanks for registering. You are now logged in.")
        user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
        login(request, user)
        if next:
            return redirect(next)
        return redirect('users:profile')

    return render(request, "users/register.html", context)


def change_sidebar_status(request):
    user = request.user
    if user.is_authenticated:
        sidebar_obj, new_obj = Sidebar.objects.new_or_get(request)
        sidebar_obj.is_opened = not sidebar_obj.is_opened
        sidebar_obj.save()
        request.session['sidebar_id_status'] = sidebar_obj.is_opened
        return HttpResponse('{}'.format(sidebar_obj.is_opened))
    else:
        return HttpResponse('sorry')
