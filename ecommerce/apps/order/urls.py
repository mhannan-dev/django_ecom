from django.urls import path
from .views import orders

urlpatterns = [
    path('index', orders, name='orders')
]
