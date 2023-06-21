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
 
# class SubscriptionsForm(forms.Form):

#     def __init__(self, user, *args, **kwargs):
#         User = get_user_model()

#         super().__init__(*args, **kwargs)
#         excluded_users = UserFollows.objects.filter(user=user).values_list('followed_user', flat=True)
#         available_users = User.objects.exclude(id__in=excluded_users)
#         followed_users = UserFollows.objects.filter(followed_user=user).values_list('user', flat=True)

#         self.fields['listAvailableUsers'] = forms.ModelMultipleChoiceField(
#             queryset=available_users,
#             label='Utilisateurs disponibles',
#             widget=forms.SelectMultiple(attrs={'class': 'form-control'})
#         )

#         self.fields['listFollowedUsers'] = forms.ModelMultipleChoiceField(
#             queryset=User.objects.filter(id__in=followed_users),
#             label='Utilisateurs suivis',
#             widget=forms.SelectMultiple(attrs={'class': 'form-control'})
#         )

#         self.fields['listFollowers'] = forms.ModelMultipleChoiceField(
#             queryset=User.objects.filter(id__in=UserFollows.objects.filter(followed_user=user).values_list('user')),
#             label='Utilisateurs qui vous suivent',
#             widget=forms.SelectMultiple(attrs={'class': 'form-control'})
#         )

class SubscriptionsForm(forms.ModelForm):

    class Meta:
        model = models.UserFollows
        fields = ['followed_user']
        labels = {'followed_user': 'Abonnements'}



# class TicketForm(forms.ModelForm):

#     def __init__(self, *args, **kwargs):
#         super(TicketForm, self).__init__(*args, **kwargs)
#         if self.instance and self.instance.image:
#             self.fields['image'].label = ''

#     class Meta:
#         model = models.Ticket
#         fields = [
#             'title',
#             'description',
#             'image'
#         ]
#         labels = {
#             'title': 'Titre',
#         }