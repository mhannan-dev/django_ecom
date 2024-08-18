from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import Product
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def index(request):
    product_list = Product.objects.filter(status=True)
    
    paginator = Paginator(product_list, 8) 
    page_number = request.GET.get('page')
    
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    context = {
        'products': products,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'index.html', context)
