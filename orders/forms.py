from django import forms

from orders.models import Order, OrderItem


class OrderItemStatusForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = [
            'status',
        ]

        widgets = {
            'status': forms.Select(attrs={'class': 'form-control', 'required': 'required', 'placeholder': ''}),
        }
        labels = {
            'status': 'Status',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
