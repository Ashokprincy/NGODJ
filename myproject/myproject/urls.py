from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('donations.urls')), # This tells Django to look at your app's urls
    path('accounts/', include('django.contrib.auth.urls')), # This handles Login/Logout
]