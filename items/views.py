from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from categories.models import Category
from items.models import Item
from users.decorators import provider_required
from items import forms

# Create your views here.


@login_required
@provider_required
def category_select(request):
    context = {}
    categories = Category.objects.all_active()
    template_name = 'items/category_select.html'
    context['objects'] = categories
    return render(request, template_name, context)
    

@login_required
@provider_required
def item_list(request,pk):
    context  = {}
    try:
        category = Category.objects.get(pk=pk, is_deleted=False)
    except category.DoesNotExist:
        messages.error(request, 'Category Not Found')
        return redirect('/')

    items = Item.objects.filter(is_deleted = False, category = category , provider=request.user.company_admin.company)
    context['objects'] = items
    context['category'] = category
    template_name = 'items/item_list.html'
    return render(request, template_name , context)


@login_required
@provider_required
def item_add(request,pk):
    context = {}
    try:
        category = Category.objects.get(pk=pk, is_deleted=False)
    except category.DoesNotExist:
        messages.error(request, 'Category Not Found')
        return redirect('/')
    if category:
        form = forms.ItemCreateForm(data=request.POST or None)
        stockForm = forms.StockForm(data=request.POST or None)
        if request.method == 'POST':
            if form.is_valid() and stockForm.is_valid():
                data = form.save(commit=False)
                data.provider = request.user.company_admin.company
                data.category = category
                data.save()
                stock = stockForm.save(commit=False)
                stock.item = data
                stock.save()
                messages.success(request, 'Item Created')
                return redirect('items:list', category.pk)
    context['category'] = category
    context['form'] = form
    context['stock_form'] = stockForm
    template_name = 'items/item_add.html'
    return render(request, template_name, context )