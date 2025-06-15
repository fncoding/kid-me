from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label="Dein Name", max_length=100, required=True)
    email = forms.EmailField(label="Deine E-Mail", required=True)
    subject = forms.CharField(label="Betreff", max_length=150, required=True)
    message = forms.CharField(label="Nachricht", widget=forms.Textarea, required=True)