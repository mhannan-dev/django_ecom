from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from apps.shopping.views import add_to_cart, cart, checkout_view, order_success, update_cart, remove_cart

urlpatterns = [
    path('cart/', cart, name='cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('update-cart/<int:product_id>/', update_cart, name='update_cart'),
    path('remove-cart/<int:product_id>/', remove_cart, name='remove_cart'),
    path('checkout/', checkout_view, name='checkout'),
    path('success/', order_success, name='order_success'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
