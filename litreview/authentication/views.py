# authentication/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import UserFollows

from . import forms


def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            # check if credentials are valid
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                # log into the server
                login(request, user)
                return redirect('post')
            else:
                message = 'Identifiants invalides.'
    return render(
        request,
        'authentication/login.html',
        context={'form': form, 'message': message}
    )

def logout_user(request):
    logout(request)
    return redirect('login')

def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})

def subscriptions(request):
    user = request.user
    followers = UserFollows.objects.filter(followed_user=user)
    return render(request, 'www/subscriptions.html', {'followers': followers})