from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from authentication.models import User
from . import forms
from .models import Ticket, Review, UserFollows


def home(request):
    return render(request, 'www/home.html')

@login_required
def new_ticket(request):
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False) # commit=False to NOT submit the save, we need to associate user before, see bellow
            ticket.user = request.user # associate user to this picture upload
            ticket.save() # and finaly save
            return redirect('flux')
    else:
        form = forms.TicketForm()
    
    return render(request, 'www/ticket.html', {'form': form})

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'www/ticket_detail.html', {'ticket': ticket})

@login_required
def flux(request):
    user = request.user
    tickets = Ticket.objects.filter(user=user)
    for ticket in tickets:
        print(ticket.time_created)
    users = User.objects.all
    usersFollows = UserFollows.objects.all
    return render(
        request,
        'www/flux.html',
        context={
            'tickets': tickets,
            'users': users,
            'usersFollows': usersFollows,
            'user_id': request.user.id
        }
    )

@login_required
def new_review(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False) # commit=False to NOT submit the save, we need to associate user before, see bellow
            ticket.user = request.user # associate user to this picture upload
            ticket.save() # and finaly save
            review = review_form.save(commit=False) # commit=False to NOT submit the save, we need to associate ticket & user before, see bellow
            review.ticket = ticket # associate ticket to this review
            review.user = request.user # associate user to this review
            review.save() # and finaly save
            return redirect('flux')
    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
        # 'is_review': True,
    }
    return render(request, 'www/review.html', context=context)

@login_required
def review_detail(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    ticket_id = review.ticket
    return render(request, 'www/review_detail.html', {'review': review, 'ticket': ticket_id})

def subscriptions(request):
    user = request.user
    followers = UserFollows.objects.filter(followed_user=user)
    return render(request, 'www/subscriptions.html', {'followers': followers})
    

