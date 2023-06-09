# authentication/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom d’utilisateur')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput())

class SignupForm(UserCreationForm):
    # delete help_text for second password fields (for my point of view : not needed)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password2'].help_text = None
    class Meta(UserCreationForm.Meta):
        pass
        model = get_user_model()
        fields = ('username', 'password1', 'password2')
