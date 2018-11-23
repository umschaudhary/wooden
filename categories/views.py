from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from categories import forms
from categories.models import Category
from users.decorators import admin_required


@login_required
@admin_required
def category_list(request):
    context = {}
    objects = Category.objects.all_active()
    template_name = 'categories/category_list.html'

    context['objects'] = objects
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


def items_category(request, slug):
    context = {}
    try:
        category = Category.objects.get(slug=slug)
    except Category.MultipleObjectsReturned:
        category = Category.objects.filter(slug=slug).first()
    except Category.DoesNotExist:
        category = None
    if category:
        items = category.items.all_active()
    context['products'] = items
    context['categories'] = Category.objects.all_active()
    template_name = 'categories/items_category.html'
    return render(request, template_name, context)
