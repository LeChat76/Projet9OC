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

class TicketDeleteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TicketDeleteForm, self).__init__(*args, **kwargs)
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
    
    rating = forms.ChoiceField(
        choices=[(str(i), str(i)) for i in range(6)],
        widget=forms.RadioSelect(attrs={'class': 'rating-radio'}),
        label='Note'
    )

    class Meta:
        model = models.Review
        fields = [
            'headline',
            'rating',
            'body',
        ]
        labels = {
            'headline':  'Titre',
            'body': 'Commentaire',
        }
