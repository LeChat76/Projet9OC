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
    followed_users = get_user_model().objects.filter(id__in=listFollowed)
    listFollowers = UserFollows.objects.filter(followed_user=user).values_list('user_id', flat=True)
    followers_users = get_user_model().objects.filter(id__in=listFollowers)
    available_users = get_user_model().objects.exclude(
        id__in=listFollowed
        ).exclude(
        id=user.id
        ).exclude(
        username=user.username
    )

    if request.method == 'POST':
        # adding an user to follow
        if 'add_subscription' in request.POST:
            followed_user_id = request.POST['followed_user']
            followed_user = get_user_model().objects.get(id=followed_user_id)
            UserFollows.objects.create(user=request.user, followed_user=followed_user)
            return redirect('subscriptions')
        if 'remove_subscription' in request.POST:
            followed_user_id = request.POST['remove_subscription']
            print('FOLLOWED', followed_user_id)
            if followed_user_id:
                followed_user_id = int(followed_user_id)
                followed_user = get_user_model().objects.get(id=followed_user_id)
                UserFollows.objects.filter(user=request.user, followed_user=followed_user).delete()
                return redirect('subscriptions')
    
    context = {
        'followed_users': followed_users,
        'followers_users': followers_users,
        'available_users': available_users,
        'form': form,
    }
    
    return render(request, 'authentication/subscriptions.html', context)




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