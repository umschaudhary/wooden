from django import forms

from companies.models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'name',
            'address',
            'city',
            'postal_code',
            'email',
            'phone_no'
        ]

        widgets = {
            'name': forms.CharField(attrs={'class': 'form-control','required':'required'}),
        }

        labels = {
            'name' : 'Company Name'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)