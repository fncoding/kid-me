from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import ContactForm

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                send_mail(
                    subject=f"Kontaktformular: {data['subject']} (von {data['name']}, {data['email']})",
                    message=data['message'],
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False, 
                )
                messages.success(request, "Danke für deine Nachricht!")
                return redirect("contact")
            except Exception as e:
                # You might want to log the error `e` here
                messages.error(request, "Entschuldigung, es gab ein Problem beim Senden deiner Nachricht. Bitte versuche es später erneut.")
                # The form with user's data will be re-rendered below
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form})
