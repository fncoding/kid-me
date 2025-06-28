from django import forms
from .models import StockList, StockListItem
from django.contrib.auth.models import User
# from products.models import Product


class StockListForm(forms.ModelForm):
    class Meta:
        model = StockList
        fields = ['name', 'owner', 'shared_with'] # owner is a ForeignKey, shared_with is ManyToManyField
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'shared_with': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'owner': forms.Select(attrs={'class': 'form-select'}),
           #'shared_with': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Stock List Name',
            'owner': 'Owner',
            'shared_with': 'Shared with',
        }

class StockListCreateForm(forms.ModelForm):
    class Meta:
        model = StockList
        fields = ['name', 'owner', 'shared_with']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'value': '{{ Stocklist.name }}'}),
            'shared_with': forms.CheckboxSelectMultiple(attrs={'class': 'form-select'}),
            'owner': forms.Select(attrs={'class': 'form-select'}),
       }
            
        labels = {
            'name': 'StockList Name',
            'owner': 'Owner',
            'shared_with': 'Shared with',
        }
      

class StockListUpdateForm(forms.ModelForm):
    class Meta:
        model = StockList
        fields = ['name', 'owner', 'shared_with']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'owner': forms.Select(attrs={'class': 'form-select'}),
            'shared_with': forms.SelectMultiple(attrs={'class': 'form-select'})
    }
        labels = {
            'name': 'Stocklist Name',
            'owner': 'Owner',
            'shared_with': 'Shared with',
   }

class StockListDetailForm(forms.ModelForm):
    class Meta:
        model = StockList
        fields = ['name', 'owner', 'shared_with']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            
    }
        labels = {
            'name': 'Stocklist Name',
     
   }

class StockListItemForm(forms.ModelForm):
    class Meta:
        model = StockListItem
        fields = ['product', 'quantity', 'is_purchased']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'is_purchased': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'product': 'Product',
            'quantity': 'Quantity',
            'is_purchased': 'Purchased',
        }