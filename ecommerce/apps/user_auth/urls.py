from django.urls import path
from .views import user_dashboard, user_logout

urlpatterns = [
    path('dashboard', user_dashboard, name='user_dashboard'),
    path('logout', user_logout, name='user_logout'),
]
