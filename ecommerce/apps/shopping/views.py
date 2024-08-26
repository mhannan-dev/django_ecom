import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import logging
from django.shortcuts import get_object_or_404
from apps.shopping.models import Cart, CartItem
from apps.main.models import Product
from django.http import JsonResponse
from django.conf import settings
from django.http import JsonResponse


logger = logging.getLogger(__name__)

@login_required
def cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)

    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.discounted_price * item.quantity for item in cart_items)

    context = {
        'title': "Carts",
        'cart_items': cart_items,
        'MEDIA_URL': settings.MEDIA_URL,
        'total_price': total_price,
    }
    return render(request, 'carts/index.html', context)
@login_required
def update_cart(request, product_id):
    try:
        data = json.loads(request.body)
        quantity_change = data.get('quantityChange', 0)
        
        if quantity_change not in [-1, 1]:
            return JsonResponse({'success': False, 'message': 'Invalid quantity change.'})
        
        cart_item = CartItem.objects.get(id=product_id)
        new_quantity = cart_item.quantity + quantity_change
        
        if new_quantity <= 0:
            cart_item.delete()
        else:
            cart_item.quantity = new_quantity
            cart_item.save()

        return JsonResponse({'success': True})
    
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Cart item does not exist.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

    
@login_required
def remove_cart(request, product_id):
    if request.method == 'POST':
        try:
            if request.user.is_authenticated:
                cart, created = Cart.objects.get_or_create(user=request.user)
            else:
                session_key = request.session.session_key
                if not session_key:
                    request.session.create()
                    session_key = request.session.session_key
                cart, created = Cart.objects.get_or_create(session_key=session_key)
            
            cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
            
            cart_item.delete()
            
            total_price = sum(item.product.discounted_price * item.quantity for item in CartItem.objects.filter(cart=cart))
            
            return JsonResponse({
                'success': True,
                'message': 'Item removed from cart successfully',
                'total_price': total_price
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

@login_required  
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'message': 'Product added to cart successfully',
            'cart_item_count': cart.items.count()
        })

    return redirect('cart')


@login_required
def checkout_view(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart = Cart.objects.filter(session_key=session_key).first()

    if not cart:
        return redirect('cart')

    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.discounted_price * item.quantity for item in cart_items)

    if request.method == "POST":
        payment_method = request.POST.get('payment_method')
        billing_address = request.POST.get('billing_address')

        if not billing_address or not payment_method:
            return render(request, 'carts/checkout.html', {
                'cart_items': cart_items,
                'total_price': total_price,
                'title': 'Checkout',
                'error_message': 'Please fill in all the required fields.',
            })

        # Here you would typically save the order details and redirect to a success page
        # You can create an Order model instance, associate it with the user and cart items,
        # then clear the cart after the order is successfully placed.
        # For example:
        # order = Order.objects.create(user=request.user, billing_address=billing_address, payment_method=payment_method)
        # for item in cart_items:
        #     OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        # cart_items.delete()  # Clear the cart

        return redirect('order_success')

    return render(request, 'carts/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'title': 'Checkout',
    })



@login_required
def order_success(request):
    return render(request, 'carts/order_success.html', {'title': 'Order Successful'})