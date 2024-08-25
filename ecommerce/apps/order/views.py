
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import logging


logger = logging.getLogger(__name__)

@login_required
def orders(request):
    context = {
        'title': "Orders",
    }
    return render(request, 'auth/orders.html', context)