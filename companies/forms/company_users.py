from django import forms

from companies.models import Company, CompanyAdmin


class CompanyUserForm(forms.ModelForm):
    class Meta:
        model = CompanyAdmin
        fields = [
            'email',
            'password',
            'full_name'
            
        ]

        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control','required':'required','placeholder':''}),
            'password': forms.TextInput(attrs={'class': 'form-control','required':'required','placeholder':''}),
            'full_name': forms.TextInput(attrs={'class': 'form-control','required':'required','placeholder':''}),
           
        }

        labels = {
            'email' : 'Email Address',
            'password':'password',
            'full_name':'Name'

          
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)