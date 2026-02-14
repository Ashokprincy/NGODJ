from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('donate/<int:campaign_id>/', views.donate, name='donate'),
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    path('register/', views.register, name='register'), # New Register Path
    path('profile/', views.profile, name='profile'),
]