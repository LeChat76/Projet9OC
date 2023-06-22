# authentication/forms.py

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from . import models

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label="Nom d'utilisateur")
    password = forms.CharField(max_length=63, label="Mot de passe", widget=forms.PasswordInput())

class SignupForm(UserCreationForm):

    username = forms.CharField(label="Nom d'utilisateur")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['password1'].widget.attrs.update({'autocomplete': 'off'})
        # delete help_text for second password fields (for my point of view : not needed)
        self.fields['password2'].help_text = None
        self.fields['password2'].widget.attrs.update({'autocomplete': 'off'})

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'password1', 'password2')
        error_messages = {
            'username': {
                'unique': "Ce nom d'utilisateur est déjà utilisé. Veuillez en choisir un autre."
            },
        }

    def clean_password2(self):

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        
        return password2
 
class SubscriptionsForm(forms.Form):

    followed_user = forms.CharField(label=False, required=True, widget=forms.TextInput(attrs={'class': 'available-container-field'}))


    class Meta:
        model = models.UserFollows
        fields = ['followed_user']
        labels = {'followed_user': 'Abonnements'}
