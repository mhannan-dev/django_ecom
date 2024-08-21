from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages



@login_required
def user_dashboard(request):
    context = {
        'title': "Dashboard"
    }
    return render(request, 'auth/dashboard.html', context)


@login_required
def user_logout(request):
    logout(request)
    return redirect('account_form')