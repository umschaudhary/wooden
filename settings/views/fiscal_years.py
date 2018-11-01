from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from settings import forms
from settings.models import FiscalYear


@login_required
def fiscal_year_list(request):
    context = {}
    fiscal_year = FiscalYear.get_active_fiscal_year()
    objects = FiscalYear.objects.filter(is_deleted=False, is_active=False)
    context['objects'] = objects
    context['active_fiscal_year'] = fiscal_year
    return render(request, 'settings/fiscal_years/fiscal_years.html', context)


@login_required
def fiscal_year_create(request):
    context = {}
    form = forms.FiscalYearForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            data = form.save(commit=False)
            fiscal_year = form.cleaned_data['is_active']
            
            if fiscal_year:
                for ay in FiscalYear.objects.filter(is_active=True, is_deleted=False):
                    ay.is_active = False
                    ay.save()
                data.is_active = True
            
            data.save()
            messages.success(request, 'आर्थिक वर्ष सिर्जना गरिएको छ।')
            return redirect('fiscal_years:list')
    context['form'] = form
    return render(request, 'settings/fiscal_years/fiscal_year_create.html', context)


@login_required
def fiscal_year_edit(request, pk):
    context = {}
    try:
        fiscal_year = FiscalYear.objects.get(pk=pk, is_deleted=False)
    except FiscalYear.DoesNotExist:
        messages.error(request, 'आर्थिक वर्ष फेला परेन |')
        return redirect('fiscal_years:list')
    form = forms.FiscalYearForm(
        request.POST or None, instance=fiscal_year)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'आर्थिक वर्ष सम्पादन गरिएको छ।')
            return redirect('fiscal_years:list')
    context['form'] = form
    return render(request, 'settings/fiscal_years/fiscal_year_edit.html', context)


@login_required
def fiscal_year_change(request):
    context = {}
    form = forms.FiscalYearChangeForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            for ay in FiscalYear.objects.filter(is_active=True, is_deleted=False):
                ay.is_active = False
                ay.save()
            fiscal_year = form.cleaned_data['fiscal_year']
            fiscal_year.is_active = True
            fiscal_year.save()
            messages.success(request, 'आर्थिक वर्ष {} मा परिवर्तन भयो। '.format(fiscal_year.name))
            return redirect(reverse('fiscal_years:list'))

    context['form'] = form
    return render(request, 'settings/fiscal_years/fiscal_year_change.html', context)
