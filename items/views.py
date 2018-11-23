import decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from carts.models import Cart, CartItem
from categories.models import Category
from comments.forms import CommentForm
from comments.models import Comment
from items import forms
from items.forms import BaseItemModelFormSet
from items.models import Item, ItemImage
from ratings.forms import RatingForm
from ratings.models import Rating
from settings.models import FiscalYear
from users.decorators import provider_required
from users.models import GuestEmail


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
def item_list(request, pk):
    context = {}
    try:
        category = Category.objects.get(pk=pk, is_deleted=False)
    except Category.DoesNotExist:
        category = None

    items = Item.objects.filter(is_deleted=False, category=category, provider=request.user.company_admin.company)

    page = request.GET.get('page', 1)
    paginator = Paginator(items, 20)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    context['objects'] = items
    context['category'] = category
    template_name = 'items/item_list.html'
    return render(request, template_name, context)


@login_required
@provider_required
def item_add(request, pk):
    context = {}
    try:
        category = Category.objects.get(pk=pk, is_deleted=False)
    except Category.DoesNotExist:
        messages.error(request, 'Category Not Found')
        return redirect('/')
    if category:
        form = forms.ItemCreateForm(data=request.POST or None)
        stockForm = forms.StockForm(data=request.POST or None)
        ItemFormSet = modelformset_factory(model=ItemImage, form=forms.ItemImageForm, formset=BaseItemModelFormSet)
        formset = ItemFormSet(request.POST or None, request.FILES or None, queryset=Item.objects.none())
        context['form'] = form
        context['formset'] = formset
        context['stock_form'] = stockForm
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
    template_name = 'items/item_add.html'
    return render(request, template_name, context)


def item_detail(request, slug):
    context = {}
    try:
        item = Item.objects.get(is_deleted=False, slug=slug)
        item_stock_count = item.stock_record.quantity

    except Item.DoesNotExist:
        item = None
        item_stock_count = None

    except Item.MultipleObjectsReturned:
        qs = Item.objects.filter(slug=slug, is_deleted=False)
        item = qs.first()
        item_stock_count = item.stock_record.quantity

    context['item_count'] = item_stock_count
    context['quantity'] = range(1, item_stock_count + 1)

    if item:
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        context['cart'] = cart_obj
        if cart_obj:
            context['items'] = cart_obj.cart_items.all()

        form = CommentForm(request.POST or None)
        quantity_form = forms.QuantityForm(request.POST or None)
        rating_form = RatingForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                data = form.save(commit=False)
                data.item = item
                data.fiscal_year = FiscalYear.get_active_fiscal_year()
                if request.user.is_authenticated:
                    if request.user.is_customer():
                        data.user = request.user
                        is_rated = Rating.objects.get(is_deleted=False, item=item, user=request.user)

                else:
                    if request.session['guest_email_id']:
                        guest_email_id = request.session['guest_email_id']
                        try:
                            g_mail = GuestEmail.objects.get(id=guest_email_id)
                        except GuestEmail.MultipleObjectsReturned:
                            g_mail = GuestEmail.objects.filter(id=guest_email_id).last()
                        except GuestEmail.DoesNotExist:
                            g_mail = None
                        data.guest_user = g_mail
                        is_rated = Rating.objects.get(is_deleted=False, item=item, guest_user=g_mail)

                data.save()
                return HttpResponseRedirect("")

            if quantity_form.is_valid():
                data = quantity_form.save(commit=False)
                data.cart = cart_obj
                data.item = item
                data.save()
                item.stock_record.quantity -= decimal.Decimal(data.quantity)
                item.stock_record.save()
                item.save()

                request.session['item_count'] = cart_obj.cart_items.all().count()
                messages.success(request, 'Item Added to Cart')
                return redirect('carts:cart')

            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.item = item
                rating.fiscal_year = FiscalYear.get_active_fiscal_year()
                if request.user.is_authenticated:
                    if request.user.is_customer():
                        rating.user = request.user

                else:
                    if request.session['guest_email_id']:
                        guest_email_id = request.session['guest_email_id']
                        try:
                            g_mail = GuestEmail.objects.get(id=guest_email_id)
                        except GuestEmail.MultipleObjectsReturned:
                            g_mail = GuestEmail.objects.filter(id=guest_email_id).last()
                        except GuestEmail.DoesNotExist:
                            g_mail = None
                        rating.guest_user = g_mail

                rating.save()
                return HttpResponseRedirect("")

        context['form'] = form
        context['rating_form'] = rating_form
        context['quantity_form'] = quantity_form

        try:
            data = CartItem.objects.get(item=item, cart=cart_obj)
            if data:
                context['data'] = 1

        except CartItem.MultipleObjectsReturned:
            data = CartItem.objects.filter(item=item, cart=cart_obj).first()
            if data:
                context['data'] = 1
        except CartItem.DoesNotExist:
            data = None
            if data:
                context['data'] = 1
            else:
                context['data'] = 0

        comments = Comment.objects.filter(item=item).order_by('-created_at')
        related_products = Item.objects.filter(is_deleted=False, category=item.category)
        context['related_products'] = related_products
        context['comments'] = comments
        ratings5 = Rating.objects.filter(is_deleted=False, item=item, rating=5).count()
        ratings4 = Rating.objects.filter(is_deleted=False, item=item, rating=4).count()
        ratings3 = Rating.objects.filter(is_deleted=False, item=item, rating=3).count()
        ratings2 = Rating.objects.filter(is_deleted=False, item=item, rating=2).count()
        ratings1 = Rating.objects.filter(is_deleted=False, item=item, rating=1).count()
        context['ratings5'] = ratings5
        context['ratings4'] = ratings4
        context['ratings3'] = ratings3
        context['ratings2'] = ratings2
        context['ratings1'] = ratings1
        if request.user.is_authenticated:
            if request.user.is_customer():
                try:
                    is_rated = Rating.objects.get(is_deleted=False, item=item, user=request.user)
                except:
                    is_rated = None
                if is_rated:
                    context['rate'] = is_rated
                    context['is_rated'] = True

        else:
            if request.session['guest_email_id']:
                guest_email_id = request.session['guest_email_id']
                try:
                    g_mail = GuestEmail.objects.get(id=guest_email_id)
                except GuestEmail.MultipleObjectsReturned:
                    g_mail = GuestEmail.objects.filter(id=guest_email_id).last()
                except GuestEmail.DoesNotExist:
                    g_mail = None
                try:
                    is_rated = Rating.objects.get(is_deleted=False, item=item, guest_user=g_mail)
                except:
                    is_rated = None
                if is_rated:
                    context['rate'] = is_rated
                    context['is_rated'] = True

    context['item'] = item
    template_name = 'items/item_detail.html'
    return render(request, template_name, context)


@login_required
@provider_required
def item_update(request, slug):
    context = {}
    try:
        item = Item.objects.get(is_deleted=False, slug=slug)
        item_stock_count = item.stock_record.quantity
    except Item.DoesNotExist:
        item = None
    except Item.MultipleObjectsReturned:
        qs = Item.objects.filter(slug=slug, is_deleted=False)
        item = qs.first()
    if item:
        stock_record = item.stock_record
    else:
        stock_record = None

    form = forms.ItemCreateForm(data=request.POST or None, instance=item)
    stockForm = forms.StockForm(data=request.POST or None, instance=stock_record)
    ItemFormSet = modelformset_factory(model=ItemImage, form=forms.ItemImageForm, formset=BaseItemModelFormSet)
    formset = ItemFormSet(request.POST or None, request.FILES or None, queryset=ItemImage.objects.none())
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
    context['stock_record'] = stock_record
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
    except ItemImage.DoesNotExist:
        image = None
        return redirect('/')
    except ItemImage.MultipleObjectsReturned:
        qs = ItemImage.objects.filter(pk=pk)
        image = qs.last()

    if image:
        image.delete()
        messages.success(request, 'Item Updated')

    return redirect('items:update', image.item.slug)
