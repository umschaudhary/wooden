from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from items import forms

from carts.models import Cart, CartItem
from categories.models import Category
from items.models import Item
from users.decorators import provider_required


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


def item_detail(request, slug):
    context = {}
    try:
        item = Item.objects.get(is_deleted=False, slug=slug)
        item_stock_count = item.stock_record.quantity
    except Item.DoesNotExist:
        messages.error(request, 'Product Not Found ')
        return redirect('/')
    except Item.MultipleObjectsReturned:
        qs = Item.objects.filter(slug=slug, is_deleted=False)
        item = qs.first()
    if item:
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if request.method == 'POST':
            quantity = request.POST['quantity']
            cart_item = CartItem()
            cart_item.cart = cart_obj
            cart_item.item = item
            cart_item.quantity = quantity 
            cart_item.save()
            item.in_cart = True
            item.save()
            messages.success(request, 'Item Added to Cart')
            return redirect('/')

    context['item'] = item
    context['quantity'] = range(1,item_stock_count+1)
    context['item_count'] = item_stock_count
    
    context['cart'] = cart_obj

    template_name = 'items/item_detail.html'
    return render(request, template_name, context)

