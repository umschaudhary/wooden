from django import forms

from companies.models import Company, CompanyCategory


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'name',
            'address',
            'city',
            'postal',
            'email',
            'phone_number'
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','required':'required','placeholder':''}),
            'address': forms.TextInput(attrs={'class': 'form-control','required':'required','placeholder':''}),
            'postal': forms.TextInput(attrs={'class': 'form-control','required':'required','placeholder':''}),
            'city': forms.TextInput(attrs={'class': 'form-control','required':'required','placeholder':''}),
            'email': forms.TextInput(attrs={'class': 'form-control','required':'required','placeholder':''}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control','required':'required','placeholder':''}),
        }

        labels = {
            'name' : 'Company Name'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class CompanyCategoryForm(forms.ModelForm):
    class Meta:
        model = CompanyCategory
        fields = [
            'category'
        ]

        widgets = {
            'category': forms.SelectMultiple(attrs={'class':'form-control', 'required':'required', 'placeholder':''})
        }

 