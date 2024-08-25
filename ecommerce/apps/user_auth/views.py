# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .forms import ProfileForm, UpdatePasswordForm
from django.contrib.auth import update_session_auth_hash
import logging


logger = logging.getLogger(__name__)

@login_required
def user_dashboard(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            logger.info('Profile updated successfully for user: %s', request.user.username)
            return redirect(request.path_info)
        else:
            messages.error(request, 'There was an error updating your profile.', form.errors)
    else:
        form = ProfileForm(instance=request.user)

    context = {
        'title': "Profile",
        'profile_form': form
    }
    return render(request, 'auth/dashboard.html', context)

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Logout successful!")
    return redirect('account_form')


@login_required
def user_password_update(request):
    if request.method == 'POST':
        form = UpdatePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            logout(request)
            return redirect('account_form')

        else:
            messages.error(request, 'Form errors: %s', form.errors)
    else:
        form = UpdatePasswordForm(user=request.user)
    context = {
        'title': "Password update",
        'pwd_update_form': form
    }
    return render(request, 'auth/user_password_update.html', context)
