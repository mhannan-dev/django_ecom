from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login
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

def index(request):
    search_query = request.GET.get('search', '')

    product_list = get_filtered_products(search_query)

    page_number = request.GET.get('page')
    products = paginate_products(product_list, page_number)

    context = {
        'products': products,
        'page_name': "home_page",
        'MEDIA_URL': settings.MEDIA_URL,
        'search_query': search_query,
    }
    return render(request, 'index.html', context)



def get_product_details(slug):
    product = get_object_or_404(Product, slug=slug)
    ratings = Rating.objects.filter(product=product)
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
                # messages.success(request, "Login successful!")
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