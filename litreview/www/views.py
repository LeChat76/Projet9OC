from itertools import chain
from django.db.models import CharField, Value
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import models, forms
from .models import Ticket, Review
from PIL import Image


def home(request):
    return render(request, 'www/home.html')

def resize_image(image, max_size):
    img = Image.open(image)
    img.thumbnail(max_size)
    return img

@login_required
def new_ticket(request):
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False) # commit=False to NOT submit the save, we need to associate user before, see bellow
            ticket.user = request.user # associate user to this picture upload
            ticket.save() # and finaly save
            return redirect('post')
    else:
        form = forms.TicketForm()
    
    return render(request, 'www/ticket.html', {'form': form})

# @login_required
# def ticket_detail(request, ticket_id):
#     ticket = get_object_or_404(Ticket, id=ticket_id)
#     return render(request, 'www/ticket_detail.html', {'ticket': ticket})

@login_required
def post(request):
    reviews = get_users_viewable_reviews(request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    tickets = get_users_viewable_tickets(request.user) 
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    posts = sorted(
        chain(tickets, reviews),
        key=lambda post: post.time_created,
        reverse=True,
    )
    
    return render(request, 'www/post.html', context={'posts': posts})

def get_users_viewable_reviews(user):
    reviews = Review.objects.filter(user=user)
    return reviews

def get_users_viewable_tickets(user):
    tickets = Ticket.objects.filter(user=user)
    return tickets

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
            return redirect('post')
    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
    }
    return render(request, 'www/review.html', context=context)

@login_required
def review_detail(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    ticket_id = review.ticket
    return render(request, 'www/review_detail.html', {'review': review, 'ticket': ticket_id})
   
@login_required
def review_edit(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    review = get_object_or_404(Review, ticket_id=ticket_id)
    review_form = forms.ReviewForm(instance=review)
    if request.method == 'POST':
        edit_form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
        review_form = forms.ReviewForm(request.POST, instance=review)
        if all([edit_form.is_valid(), review_form.is_valid()]):
            edited_ticket = edit_form.save(commit=False)
            edited_ticket.user = request.user
            edited_ticket.save()
            review = review_form.save(commit=False)
            review.ticket = edited_ticket
            review.user = request.user
            review.save()
            return redirect('post')
    context = {
        'edit_form': edit_form,
        'review_form': review_form,
    }
    return render(request, 'www/review_edit.html', context=context)

@login_required
def ticket_edit(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    if request.method == 'POST':
        edit_form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
        if edit_form.is_valid():
            edited_ticket = edit_form.save(commit=False)
            edited_ticket.user = request.user
            edited_ticket.save()
            return redirect('post')
    context = {
        'edit_form': edit_form,
    }
    return render(request, 'www/ticket_edit.html', context=context)

@login_required
def flux(request):
    return render(request, 'www/flux.html')
