from django.urls import path

from apps.main.views import account_form, index, submit_rating,product_detail


urlpatterns = [
    path('', index, name='home'),
    path('account/', account_form, name='account_form'),  
    path('submit-rating/<slug:slug>/', submit_rating, name='submit_rating'),
    path('<slug:slug>/', product_detail, name='product_detail'),
]
