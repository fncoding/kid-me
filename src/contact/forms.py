from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        label="Dein Name",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="Deine E-Mail",
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    subject = forms.CharField(
        label="Betreff",
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        label="Nachricht",
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        required=True
    )