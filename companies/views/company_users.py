from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from companies import forms
from companies.models import Company, CompanyAdmin
from users.models import USER_ROLES, User


@login_required
def company_users(request, pk):
    context = {}
    try:
        company = Company.objects.get(pk=pk, is_deleted=False)
    except:
        messages.error(request,'Not Found')
        return redirect('companies:list')
    if company:
        users = company.company_admins.all_active()
        inactive_users = company.company_admins.filter(is_deleted=True)
    context['objects'] = users
    context['company'] = company
    context['inactive_users'] = inactive_users
    template_name = 'company_users/company_users.html'
    return render(request, template_name, context)

@login_required
def company_user_create(request,pk):
    context = {}
    try:
        company = Company.objects.get(pk=pk, is_deleted=False)
    except:
        messages.error(request,'Not Found')
        return redirect('companies:list')
    if company: 
        form = forms.CompanyUserForm(data=request.POST or None)
        if request.method == 'POST':
            if form.is_valid:
                cuser = form.save(commit=False)
                cuser.company = company
                cuser.save()
                user = User()
                user.email = cuser.email
                user.full_name = cuser.full_name
                user.role = USER_ROLES.provider
                user.set_password(cuser.password)
                user.save()
                cuser.user = user
                cuser.save()
                messages.success(request,'User created Successfully')
                return redirect('company_users:list', company.pk)
        context['form'] = form
        template_name = 'company_users/company_user_create.html'
    return render(request, template_name, context)


@login_required
def company_user_change_status(request, pk):
    context = {}
    try:
        cuser = CompanyAdmin.objects.get(pk=pk)
    except CompanyAdmin.DoesNotExist:
        messages.error(request, "Company Admin Not Found")
        return redirect('companies:list')
    if cuser:
        if request.method == 'POST':
            cuser.is_deleted = not cuser.is_deleted
            cuser.save()
            messages.success(request,'User status Changed ')
            return redirect('company_users:list',cuser.company.pk)
    context['user'] = cuser
    
    template_name = 'company_users/change_status.html'
    return render(request, template_name, context)