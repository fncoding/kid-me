from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewUserForm, UsernameChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from .tokens import account_activation_token
from django.contrib.auth.models import User

def home_view(request):
    return render(request, 'login/home.html')

@login_required
def dashboard_view(request):
    return render(request, 'login/dashboard.html')

def register_view(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  
            user.save()
            # Send activation email
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            activation_link = request.build_absolute_uri(
                f"/activate/{uid}/{token}/"
            )
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'activation_link': activation_link,
            })
            send_mail(
                'Activate your account',
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            messages.success(request, 'Please confirm your email address to complete the registration.')
            return redirect('home')
        messages.error(request, 'Unsuccessful registration. Invalid information.')
    else:
        form = NewUserForm()
    return render(request, 'login/register.html', context={'form': form})


@login_required
def username_change_view(request):
    if request.method == 'POST':
        form = UsernameChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Benutzername geändert.')
            return redirect('dashboard')
    else:
        form = UsernameChangeForm(instance=request.user)
    return render(request, 'login/username_change.html', {'form': form})

@login_required
def profile_edit_view(request):
    username_form = UsernameChangeForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)

    if request.method == 'POST':
        if 'username_submit' in request.POST:
            username_form = UsernameChangeForm(request.POST, instance=request.user)
            if username_form.is_valid():
                username_form.save()
                messages.success(request, 'Benutzername geändert.')
                return redirect('profile_edit')
        elif 'password_submit' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Passwort geändert.')
                return redirect('profile_edit')

    return render(request, 'login/profile_edit.html', {
        'username_form': username_form,
        'password_form': password_form,
    })

def activate_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated. You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('home')

def contact(request):
    if request.method == "POST":
        email = request.POST.get("email")
        message = request.POST.get("message")
        if email and message:
            # Beispiel: E-Mail an dich selbst senden
            send_mail(
                subject=f"Kontaktformular von {email}",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )
            messages.success(request, "Danke für deine Nachricht!")
        else:
            messages.error(request, "Bitte alle Felder ausfüllen.")
        return redirect(request.META.get("HTTP_REFERER", "/"))