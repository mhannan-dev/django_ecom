from django.db import IntegrityError, DatabaseError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Product, Rating
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegistrationForm, CustomAuthenticationForm
import logging
logger = logging.getLogger(__name__)


def index(request):
    search_query = request.GET.get('search', '')

    product_list = get_filtered_products(search_query)

    page_number = request.GET.get('page')
    products = paginate_products(product_list, page_number)

    last_visited_product = None
    if 'last_visited_product_id' in request.session:
        last_visited_product_id = request.session['last_visited_product_id']
        try:
            last_visited_product = Product.objects.get(id=last_visited_product_id)
        except Product.DoesNotExist:
            logger.warning(f"Product with ID {last_visited_product_id} not found.")
            del request.session['last_visited_product_id']

    context = {
        'products': products,
        'page_name': "home_page",
        'MEDIA_URL': settings.MEDIA_URL,
        'search_query': search_query,
        'last_visited_product': last_visited_product 
    }
    return render(request, 'index.html', context)


def get_filtered_products(search_query):
    product_list = Product.objects.filter(status=True)
    if search_query:
        product_list = product_list.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    return product_list

def paginate_products(product_list, page_number, items_per_page=8):
    paginator = Paginator(product_list, items_per_page)
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return products

def get_product_details(slug):
    product = get_object_or_404(Product, slug=slug)
    ratings = Rating.objects.filter(product=product, status=1)
    images = product.images.all()
    return product, ratings, images

def get_suggested_products(category_id, exclude_product_id):
    return Product.objects.filter(category_id=category_id).exclude(id=exclude_product_id).order_by('-created_at')[:8]


def product_detail(request, slug):
    """Render the product detail page."""
    product, ratings, images = get_product_details(slug)
    suggested_products = get_suggested_products(product.category_id, product.id)
    
    context = {
        'product': product,
        'MEDIA_URL': settings.MEDIA_URL,
        'ratings': ratings,
        'images': images,
        'suggested_products': suggested_products
    }
    
    return render(request, 'product_detail.html', context)


    
def account_form(request):
    if request.method == 'POST':
        reg_form = RegistrationForm(request.POST)
        login_form = CustomAuthenticationForm(request, data=request.POST)

        # Handle registration
        if 'register' in request.POST and reg_form.is_valid():
            first_name = reg_form.cleaned_data['first_name']
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name)
            user.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect(request.path_info)

        # Handle login
        elif 'login' in request.POST and login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('user_dashboard') 
            else:
                messages.error(request, "Invalid username or password")

    else:
        reg_form = RegistrationForm()
        login_form = CustomAuthenticationForm()

    context = {
        'reg_form': reg_form,
        'login_form': login_form,
        'login' : "Login",
        'register': 'Register'
    }

    return render(request, 'account.html', context)




@login_required
def submit_rating(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        rating_value = request.POST.get('rating')
        review_text = request.POST.get('review')

        print(f"Rating Value: {rating_value}, Review Text: {review_text}")
        
        # Check if rating_value is provided and is valid
        if not rating_value or not rating_value.isdigit():
            messages.error(request, 'Rating value is required and must be a number between 1 and 5.')
            return redirect('product_detail', slug=slug)

        try:
            rating_value = int(rating_value)
            if rating_value < 1 or rating_value > 5:
                messages.error(request, 'Invalid rating value. Please choose a value between 1 and 5.')
                return redirect('product_detail', slug=slug)

            try:
                rating, created = Rating.objects.get_or_create(user=request.user, product=product)
                rating.rating = rating_value
                rating.review = review_text
                rating.save()

                if created:
                    logger.info('Rating created for user: %s, product: %s', request.user.username, product.name)
                else:
                    logger.info('Rating updated for user: %s, product: %s', request.user.username, product.name)

                messages.success(request, 'Your rating has been submitted successfully!')
                return redirect('product_detail', slug=slug)

            except IntegrityError as e:
                messages.error(request, 'A database integrity error occurred. Please try again.')
                logger.info(request.POST.get('rating'))
                logger.error('Integrity error when saving rating for user: %s, product: %s, Error: %s', request.user.username, product.name, str(e))
                return redirect('product_detail', slug=slug)

            except DatabaseError as e:
                messages.error(request, 'A database error occurred. Please try again later.')
                logger.error('Database error when saving rating for user: %s, product: %s, Error: %s', request.user.username, product.name, str(e))
                return redirect('product_detail', slug=slug)

        except (TypeError, ValueError):
            messages.error(request, 'Invalid rating value. Please choose a value between 1 and 5.')
            return redirect('product_detail', slug=slug)
    
    messages.error(request, 'Invalid request method.')
    return redirect('product_detail', slug=slug)


