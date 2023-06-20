# authentication/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
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
                login(request, user) # log into the server
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
            login(request, user) # auto-login user
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})

@login_required
def subscriptions(request):
    form = forms.SubscriptionsForm()
    user = request.user
    listFollowed = UserFollows.objects.filter(user=user).values_list('followed_user', flat=True)
    listFollowers = UserFollows.objects.filter(followed_user=user).values_list('user_id', flat=True)
    listAvailable = get_user_model().objects.exclude(id__in=listFollowed).exclude(id=user.id).values_list('id', flat=True)
    if request.method == 'POST':
        form = forms.SubscriptionsForm(request.POST)
        
    context = {
            'listFollowed': listFollowed,
            'listFollowers': listFollowers,
            'listAvailable': listAvailable,
    }
    return render(request, 'authentication/subscriptions.html', {'forms': form, 'listFollowed': listFollowed, 'listFollowers': listFollowers, 'listAvailable': listAvailable})


# def new_ticket(request):
#     if request.method == 'POST':
#         form = forms.TicketForm(request.POST, request.FILES)
#         if form.is_valid():
#             ticket = form.save(commit=False) # commit=False to NOT submit the save, we need to associate user before, see bellow
#             ticket.user = request.user # associate user to this picture upload
#             ticket.save() # and finaly save
#             return redirect('post')
#     else:
#         form = forms.TicketForm()
    
#     return render(request, 'www/ticket.html', {'form': form})