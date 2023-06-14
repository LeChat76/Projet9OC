from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import forms, models
from .models import Ticket, Review


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
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        form = forms.TicketForm()
    
    return render(request, 'www/ticket.html', {'form': form, 'is_review': False})

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'www/ticket_detail.html', {'ticket': ticket})

@login_required
def flux(request):
    user = request.user
    tickets = Ticket.objects.filter(user=user)
    return render(request, 'www/flux.html', context={'tickets': tickets})

@login_required
def review(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False) # commit=False to NOT submit the save, we need to associate user before, see bellow
            ticket.user = request.user # associate user to this picture upload
            ticket.save() # and finaly save
            review = review_form.save(commit=False) # commit=False to NOT submit the save, we need to associate ticket before, see bellow
            review.ticket = ticket # associate ticket to this review
            review.user = request.user
            review.save() # and finaly save
            return redirect('review_detail', review_id=review.id)
    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
        'is_review': True,
    }
    return render(request, 'www/review.html', context=context)

@login_required
def review_detail(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    ticket_id = review.ticket
    return render(request, 'www/review_detail.html', {'review': review, 'ticket': ticket_id})
