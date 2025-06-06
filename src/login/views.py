from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import NewUserForm

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