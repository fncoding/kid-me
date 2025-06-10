from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .views import profile_edit_view

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='login/password_change.html',
        success_url='/'
    ), name='password_change'),
    path('username_change/', views.username_change_view, name='username_change'),
    path('profile/', profile_edit_view, name='profile_edit'),
]