from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Product, Rating
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegistrationForm
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
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']            
            user = User.objects.create_user(username=email, email=email, password=password)
            user.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect(request.path_info)
    else:
        form = RegistrationForm()

    return render(request, 'account.html', {'form': form})