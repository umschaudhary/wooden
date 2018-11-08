
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from companies import forms
from companies.models import Company
from users.decorators import provider_required


@login_required
def category_select(request):
    context = {}
    user = request.user
    try:
        instance = Company.objects.first()
    except Company.DoesNotExist:
        instance = None

    form  = forms.CompanyCategoryForm(request.POST or None, instance=instance)
    if request.method == 'POST':
        if form.is_valid():
            data = form.save(commit=False)
            data.company = user.company_admin.company
            data.save()
            messages.success(request, 'Selected ')
            return redirect('/')
    context['form'] = form
    template_name = 'companies/category_select.html'
    return render(request, template_name , context)