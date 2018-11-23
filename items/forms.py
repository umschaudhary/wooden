from django import forms
from django.forms import BaseModelFormSet, BaseFormSet

from carts.models import CartItem
from items.models import Item, StockRecord, ItemImage


class BaseItemModelFormSet(BaseModelFormSet):
    def clean(self):
        super(BaseItemModelFormSet, self).clean()


class BaseItemFormSet(BaseFormSet):
    def save(self, commit=True):
        for form in self.forms:
            print(form.cleaned_data)
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description', '')

            item = Item(name=name, description=description)
            item.save()
        return self.forms


class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'name',
            'description',
            'featured',
            'specification'
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': ''}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'required': 'required', 'placeholder': '', 'row': 1}),
            'specification': forms.Textarea(
                attrs={'class': 'form-control', 'required': 'required', 'placeholder': '', 'row': 1}),

        }

        labels = {
            'name': 'Item Name',
            'description': 'Description',
            'featured': 'Featured It'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class StockForm(forms.ModelForm):
    class Meta:
        model = StockRecord
        fields = [
            'price_excl_tax',
            'discount_percentage',
            'quantity',
        ]

        widgets = {
            'price_excl_tax': forms.TextInput(
                attrs={'class': 'form-control', 'required': 'required', 'placeholder': ''}),
            'discount_percentage': forms.TextInput(
                attrs={'class': 'form-control', 'required': 'required', 'placeholder': ''}),
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': ''})

        }

        labels = {
            'name': 'Item Name',
            'discount_percentage': 'Discount Percent',
            'quantity': 'Stock Quantity'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class QuantityForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = [
            'quantity',
        ]

        widgets = {
            'quantity': forms.Select(
                attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Quantity'})

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['quantity'].queryset = [1,2,3,4]


class ItemImageForm(forms.ModelForm):
    class Meta:
        model = ItemImage
        fields = [
            'document',
        ]
