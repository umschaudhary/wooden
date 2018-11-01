from django import forms
from settings.models import FiscalYear

class FiscalYearForm(forms.ModelForm):
    
    class Meta:
        model = FiscalYear

        fields = [
            'name',
           'is_active'
        ]
        

        labels = {
            'is_active' : 'Active',
            'name': 'Fiscal Year'
        }

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','required':'required','placeholder':''}),
        }

class FiscalYearChangeForm(forms.Form):
    fiscal_year = forms.ModelChoiceField(queryset=FiscalYear.objects.filter(is_active=False, is_deleted=False),
                                         widget=forms.Select(attrs={'class': 'form-control'}))

    