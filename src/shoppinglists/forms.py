from django import forms
from .models import ShoppingList, ShoppingListItem
from django.contrib.auth.models import User
# from products.models import Product


class ShoppingListForm(forms.ModelForm):
    class Meta:
        model = ShoppingList
        fields = ['name', 'owner', 'shared_with'] # owner is a ForeignKey, shared_with is ManyToManyField
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'shared_with': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'owner': forms.Select(attrs={'class': 'form-select'}),
           #'shared_with': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Shopping List Name',
            'owner': 'Owner',
            'shared_with': 'Shared with',
        }

class ShoppingListCreateForm(forms.ModelForm):
    class Meta:
        model = ShoppingList
        fields = ['name', 'owner', 'shared_with']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'value': '{{ shoppinglist.name }}'}),
            'shared_with': forms.CheckboxSelectMultiple(attrs={'class': 'form-select'}),
            'owner': forms.Select(attrs={'class': 'form-select'}),
       }
            
        labels = {
            'name': 'ShoppingList Name',
            'owner': 'Owner',
            'shared_with': 'Shared with',
        }
      

class ShoppingListUpdateForm(forms.ModelForm):
    class Meta:
        model = ShoppingList
        fields = ['name', 'owner', 'shared_with']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'owner': forms.Select(attrs={'class': 'form-select'}),
            'shared_with': forms.SelectMultiple(attrs={'class': 'form-select'})
    }
        labels = {
            'name': 'Shoppinglist Name',
            'owner': 'Owner',
            'shared_with': 'Shared with',
   }

class ShoppingListDetailForm(forms.ModelForm):
    class Meta:
        model = ShoppingList
        fields = ['name', 'owner', 'shared_with']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            
    }
        labels = {
            'name': 'Shoppinglist Name',
     
   }

class ShoppingListItemForm(forms.ModelForm):
    class Meta:
        model = ShoppingListItem
        fields = ['product', 'quantity', 'is_purchased']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_purchased': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'product': 'Product',
            'quantity': 'Quantity',
            'is_purchased': 'Is Purchased',
        }

class ShoppingListCreateForm(forms.ModelForm):
    class Meta:
        model = ShoppingListItem
        fields = ['product', 'quantity', 'is_purchased']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_purchased': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'product': 'Product',
            'quantity': 'Quantity',
            'is_purchased': 'Is Purchased',
        }