from itertools import chain
from django.db.models import CharField, Value, Case, When
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import forms
from .models import Ticket, Review
from authentication.models import UserFollows


def get_users_viewable_reviews(users):
    if isinstance(users, list):
        reviews = Review.objects.filter(user__in=users)
    else:
        reviews = Review.objects.filter(user=users)
    return reviews

def get_users_viewable_tickets(users):
    if isinstance(users, list):
        tickets = Ticket.objects.filter(user__in=users)
    else:
        tickets = Ticket.objects.filter(user=users)
    return tickets

@login_required
def flux(request):
    followed_users = UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)
    followed_users = list(followed_users) + [request.user.id]
    # print('TYPE : ',(type(followed_users)))
    # print('FOLLOWED_USERS : ', followed_users)
    # print('USER_ID : ', request.user.id)
    reviews = get_users_viewable_reviews(list(followed_users))
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    tickets = get_users_viewable_tickets(list(followed_users)).annotate(
        content_type=Case(
            When(review__isnull=False, then=Value('TICKET_WR')),
            default=Value('TICKET_WOR'),
            output_field=CharField()
        )
    )

    print('TICKETS : ', tickets)

    flux = sorted(
        chain(tickets, reviews),
        key=lambda post: post.time_created,
        reverse=True,
    )

    return render(request, 'www/flux.html', context={'flux': flux})


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
def ticket_delete(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    confirm = request.POST.get('confirm')

    if confirm == 'oui':
        ticket.delete()
        return redirect('post')
    elif confirm == 'non':
        return redirect('post')

    return render(request, 'www/ticket_delete.html', {'ticket': ticket})

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
    }
    return render(request, 'www/review.html', context=context)
   
@login_required
def review_edit(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review_form = forms.ReviewForm(instance=review)
    ticket = get_object_or_404(Ticket, id=review.ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    if ticket.user == review.user:
        same_creator = True
    else:
        same_creator = False

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
        'same_creator': same_creator,
    }

    print('SAME_CREATOR : ', same_creator)

    return render(request, 'www/review_edit.html', context=context)

@login_required
def review_delete(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    ticket = get_object_or_404(Ticket, id=review.ticket_id)

    confirm = request.POST.get('confirm')

    if confirm == 'oui':
        ticket.delete()
        return redirect('post')
    elif confirm == 'non':
        return redirect('post')

    return render(request, 'www/review_delete.html', {'ticket': ticket, 'review': review})

@login_required
def ticket_create_review(request, ticket_id):
    review_form = forms.ReviewForm()
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('flux')
    context = {
        'ticket': ticket,
        'review_form': review_form,

    }
    return render(request, 'www/ticket_create_review.html', context=context)