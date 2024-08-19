from django.urls import path
from .views import index, product_detail, account_form

urlpatterns = [
    path('', index, name='home'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('account', account_form, name='account_form'),
]
