from django.urls import path

from .views import index, product_detail, account_form, submit_rating

urlpatterns = [
    path('', index, name='home'),
    path('account/', account_form, name='account_form'),  
    path('submit-rating/<slug:slug>/', submit_rating, name='submit_rating'),
    path('<slug:slug>/', product_detail, name='product_detail'),
]
