from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import forms
from .models import Ticket


def home(request):
    return render(request, 'www/home.html')

@login_required
def new_ticket(request):
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        form = forms.TicketForm()
    
    return render(request, 'www/ticket.html', {'form': form})

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'www/ticket_detail.html', {'ticket': ticket})