from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')), # Include our app's URLs
    path('accounts/', include('django.contrib.auth.urls')), # Include Django's auth URLs for login/logout
]