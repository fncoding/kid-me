from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import NewUserForm, UsernameChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def home_view(request):
    return render(request, 'login/home.html')

@login_required
def dashboard_view(request):
    return render(request, 'login/dashboard.html')

def register_view(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('dashboard')
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