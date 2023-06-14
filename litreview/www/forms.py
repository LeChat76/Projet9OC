# www/forms.py

from django.forms import ModelForm
from . import models

class TicketForm(ModelForm):

    class Meta:
        model = models.Ticket
        fields = [
            'title',
            'description',
            'image'
        ]
        labels = {
            'title': 'Titre',
        }

class ReviewForm(ModelForm):
    
    class Meta:
        model = models.Review
        fields = [
            'headline',
            'rating',
            'body',
        ]
        labels = {
            'headline':  'Titre',
            'rating': 'note',
            'body': 'commentaire',
        }
