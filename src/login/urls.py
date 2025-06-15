from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views
from .views import profile_edit_view, activate_view

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
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='pw-reset/password_reset_form.html'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='pw-reset/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='pw-reset/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='pw-reset/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('activate/<uidb64>/<token>/', activate_view, name='activate'),
]