from django import forms

from addresses.models import Address
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            # 'billing_profile',
            # 'address_type',
            'address_line_1',
            'address_line_2',
            'city',
            'country',
            
            'postal_code'
        ]

        widgets = {
            'address_line_1' : forms.TextInput(attrs={'class':'form-control'}),
            'address_line_2' : forms.TextInput(attrs={'class':'form-control'}),
            'city' : forms.TextInput(attrs={'class':'form-control'}),
            
            'postal_code' : forms.TextInput(attrs={'class':'form-control'}),
        }
