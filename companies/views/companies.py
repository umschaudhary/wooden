from companies import forms
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render

from companies.models import Company
from users.decorators import admin_required


@login_required
@admin_required
def company_list(request):
    context = {}
    objects = Company.objects.all_active()
    template_name ='companies/company_list.html'
    context ['objects'] = objects
    return render(request, template_name, context)


@login_required
@admin_required
def company_create(request):
    context = {}
    form = forms.CompanyForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            messages.success(request, 'Company Created Successfully . ')
            return redirect('companies:list')
    context['form'] = form
    return render(request, 'companies/company_create.html', context)

