
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from companies import forms
from users.decorators import provider_required


@login_required
def category_select(request):
    context = {}
    user = request.user
    form  = forms.CompanyCategoryForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Selected ')
            return redirect('/')
            3
    context['form'] = form
    template_name = 'companies/category_select.html'
    return render(request, template_name , context)