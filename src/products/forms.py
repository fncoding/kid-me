from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'amount', 'checked']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 40}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'checked': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Product Name',
            'description': 'Description',
            'price': 'Price',
            'amount': 'Amount',
            'checked': 'Checked',
        }

class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'amount', 'checked']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 40}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'checked': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Product Name',
            'description': 'Description',
            'price': 'Price',
            'amount': 'Amount',
            'checked': 'Checked',
        }


