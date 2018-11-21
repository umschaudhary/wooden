import decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.shortcuts import redirect, render

from carts.models import Cart, CartItem
from categories.models import Category
from items import forms
from items.forms import BaseItemModelFormSet
from items.models import Item, ItemImage
from users.decorators import provider_required


# Create your views here.


@login_required
@provider_required
def category_select(request):
    context = {}
    categories = Category.objects.all_active()
    template_name = 'items/category_select.html'
    context['objects'] = categories
    context['count'] = 0
    return render(request, template_name, context)
    

@login_required
@provider_required
def item_list(request,pk):
    context = {}
    try:
        category = Category.objects.get(pk=pk, is_deleted=False)
    except Category.DoesNotExist:
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
        ItemFormSet = modelformset_factory(model=ItemImage, form=forms.ItemImageForm, formset=BaseItemModelFormSet)
        formset = ItemFormSet(request.POST or None,request.FILES or None, queryset=Item.objects.none())
        if request.method == 'POST':
            if form.is_valid() and stockForm.is_valid() and formset.is_valid():
                data = form.save(commit=False)
                data.provider = request.user.company_admin.company
                data.category = category
                data.save()
                stock = stockForm.save(commit=False)
                stock.item = data
                stock.save()

                for image_form in formset.forms:
                    cd = image_form.cleaned_data
                    item_image = image_form.save(commit=False)
                    item_image.item = data
                    item_image.save()

                messages.success(request, 'Item Created')
                return redirect('items:list', category.pk)
    context['category'] = category
    context['form'] = form
    context['formset'] = formset
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
        if cart_obj:
            context['items'] = cart_obj.cart_items.all()
        if request.method == 'POST':
            quantity = request.POST['quantity']
            cart_item = CartItem()
            cart_item.cart = cart_obj
            cart_item.item = item
            cart_item.quantity = quantity 
            cart_item.save()
            
            item.stock_record.quantity -= decimal.Decimal(quantity)
            item.stock_record.save()
            item.save()

            request.session['item_count'] = cart_obj.cart_items.all().count()
            messages.success(request, 'Item Added to Cart')
            return redirect('carts:cart')
    try:
        data = CartItem.objects.get(item=item,cart=cart_obj)
        if data:
            context['data'] = 1
        
    except CartItem.MultipleObjectsReturned:
        data = CartItem.objects.filter(item=item,cart=cart_obj).first()
        if data:
            context['data'] = 1
    except CartItem.DoesNotExist:
        data = None
        if data:
            context['data'] = 1
        else:
            context['data'] = 0
    

    context['item'] = item
    context['quantity'] = range(1,item_stock_count+1)
    context['item_count'] = item_stock_count
    context['cart'] = cart_obj

    template_name = 'items/item_detail.html'
    return render(request, template_name, context)



@login_required
@provider_required
def item_update(request,slug):
    context = {}
    try:
        item = Item.objects.get(is_deleted=False, slug=slug)
        item_stock_count = item.stock_record.quantity
    except Item.DoesNotExist:
        messages.error(request, 'Item Not Found ')
        return redirect('/')
    except Item.MultipleObjectsReturned:
        qs = Item.objects.filter(slug=slug, is_deleted=False)
        item = qs.first()
    if item:
        try:
            stock_record = item.stock_record
        except:
            stock_record = None

    form = forms.ItemCreateForm(data=request.POST or None, instance=item)
    stockForm = forms.StockForm(data=request.POST or None, instance=stock_record)
    ItemFormSet = modelformset_factory(model=ItemImage, form=forms.ItemImageForm, formset=BaseItemModelFormSet)
    formset = ItemFormSet(request.POST or None,request.FILES or None, queryset=ItemImage.objects.none())
    if request.method == 'POST':
        if form.is_valid() and stockForm.is_valid() and formset.is_valid():
            form.save()
            stockForm.save()
            for image_form in formset.forms:
                cd = image_form.cleaned_data
                item_image = image_form.save(commit=False)
                item_image.item = item
                item_image.save()

            messages.success(request, 'Item Updated')
            return redirect('items:list', item.category.pk)
    images = ItemImage.objects.filter(item=item)
    context['images'] = images
    context['stock_record']  = stock_record
    context['item'] = item
    context['form'] = form
    context['formset'] = formset
    context['stock_form'] = stockForm
    template_name = 'items/item_update.html'
    return render(request, template_name, context)

@login_required
@provider_required
def image_remove(request, pk):
    context = {}
    try:
        image = ItemImage.objects.get(pk=pk)
    except ItemImage.DoesNOtExist:
        image = None
        return redirect('/')
    except ItemImage.MultipleObjectsReturned:
        qs = ItemImage.objects.filter(pk=pk)
        if qs:
            image = qs.last()

    if image :
        image.delete()
        messages.success(request, 'Item Updated')
        
    return redirect('items:update',image.item.slug)