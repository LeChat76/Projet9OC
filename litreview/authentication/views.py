# authentication/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import UserFollows, User
from django.contrib import messages

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
                return redirect('flux')
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
    context = {}

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
        # adding an user to follow from list
        if 'add_subscription' in request.POST:
            followed_user_id = request.POST['followed_user']
            followed_user = get_user_model().objects.get(id=followed_user_id)
            UserFollows.objects.create(user=request.user, followed_user=followed_user)
        
        # adding an user to follow from input
        if 'add_subscription2' in request.POST:
            followed_user_name = request.POST['followed_user_name']
            try:
                requested_user = get_user_model().objects.get(username__iexact=followed_user_name)
            except:
                print('PAS TROUVE')
                messages.error(request, 'Aucun utilisateur trouvé')
            else:
                if requested_user == request.user:
                    messages.error(request, 'Vous VOUS suivez deja ;-)')
                elif requested_user not in available_users:
                    messages.error(request, 'Vous suivez déjà cet utilisateur')
                else:
                    for available_user in available_users:           
                        if requested_user == available_user:
                            UserFollows.objects.create(user=request.user, followed_user=available_user)
            return redirect('subscriptions')
        
        # remove user from click on button
        if 'remove_subscription' in request.POST:
            followed_user_id = int(request.POST['remove_subscription'])
            followed_user = get_user_model().objects.get(id=followed_user_id)
            context = {
                'followed_user': followed_user,
            }
            return render(request, 'authentication/unsubscribe.html', context)
    
        if 'confirmYes' in request.POST:
            followed_user = request.POST['confirmYes']
            followed_user_id = get_user_model().objects.get(username=followed_user)
            UserFollows.objects.filter(user=request.user, followed_user=followed_user_id).delete()
            print('FOLLOWED_USER', followed_user)

    context = {
        'followed_users': followed_users,
        'followers_users': followers_users,
        'available_users': available_users,
        'form': form,
    }

    return render(request, 'authentication/subscriptions.html', context)
