
from categories import forms
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render

from categories.models import Category
from users.decorators import admin_required


@login_required
@admin_required
def category_list(request):
    context = {}
    objects = Category.objects.all_active()
    template_name ='categories/category_list.html'

    context ['objects'] = objects
    return render(request, template_name, context)


@login_required
@admin_required
def category_create(request):
    context = {}
    form = forms.CategoryForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            messages.success(request, 'Category Created Successfully . ')
            return redirect('categories:list')
    context['form'] = form
    return render(request, 'categories/category_create.html', context)

