from django import forms
from categories.models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name',
            'description',
           ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','required':'required','placeholder':''}),
            'description': forms.Textarea(attrs={'class': 'form-control','required':'required','placeholder':'Description ...'}),
           
        }

        labels = {
            'name' : 'Category Name',
            'description' : 'Description'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        