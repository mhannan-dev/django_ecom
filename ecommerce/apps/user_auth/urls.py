from django.urls import path
from .views import user_dashboard, user_logout, user_password_update

urlpatterns = [
    path('dashboard', user_dashboard, name='user_dashboard'),
    path('logout', user_logout, name='user_logout'),
    path('password_update', user_password_update, name='user_password_update')
]
