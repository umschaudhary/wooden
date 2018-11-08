from django import forms

from items.models import Item, StockRecord
from carts.models import CartItem, Cart


class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'name',
            'description',
            'featured',
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','required':'required','placeholder':''}),
            'description': forms.Textarea(attrs={'class': 'form-control','required':'required','placeholder':'','row':1}),
            
        }

        labels = {
            'name' : 'Item Name' , 
            'description' : 'Description',
            'featured' : 'Featured It'
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
            'price_excl_tax': forms.TextInput(attrs={'class': 'form-control','required':'required','placeholder':''}),
            'discount_percentage': forms.TextInput(attrs={'class': 'form-control','required':'required','placeholder':''}),
            'quantity' : forms.TextInput(attrs={'class':'form-control', 'required':'required','placeholder':''})
            
        }

        labels = {
            'name' : 'Item Name' , 
            'discount_percentage' : 'Discount Percent',
            'quantity' : 'Stock Quantity'
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
            'quantity' : forms.TextInput(attrs={'class':'form-control', 'required':'required','placeholder':'Quantity'})
            
        }

        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

