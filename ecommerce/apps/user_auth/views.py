from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
import logging
from .forms import ProfileForm, UpdatePasswordForm

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
            messages.error(request, 'There was an error updating your profile.')
            logger.error('Error updating profile for user: %s. Errors: %s', request.user.username, form.errors)
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
            messages.success(request, "Password updated successfully!")
            logger.info('Password updated successfully for user: %s', request.user.username)
            return redirect('account_form')
        else:
            messages.error(request, 'There was an error updating your password.')
            logger.error('Error updating password for user: %s. Errors: %s', request.user.username, form.errors)
    else:
        form = UpdatePasswordForm(user=request.user)
    
    context = {
        'title': "Password update",
        'pwd_update_form': form
    }
    return render(request, 'auth/user_password_update.html', context)

