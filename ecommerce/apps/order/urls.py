from django.urls import path
from .views import orders

urlpatterns = [
    path('list', orders, name='orders')
]
