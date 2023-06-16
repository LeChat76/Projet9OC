# www/forms.py

from django import forms
from . import models

class TicketForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.image:
            self.fields['image'].label = ''

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

class ReviewForm(forms.ModelForm):
    
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
