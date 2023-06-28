# authentication/validators.py
from django.core.exceptions import ValidationError

class ContainsLetterValidator:
    def validate(self, password, user=None):
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir une lettre', code='password_no_letters'
            )
    
    def get_help_text(self):
        return 'Votre mot de passe doit contenir au moins une lettre.'
        

class ContainsNumberValidator:              
    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir au moins un chiffre', code='password_no_numbers'
            )
    
    def get_help_text(self):
        return 'Votre mot de passe doit contenir au moins un chiffre.'

class ContainsUpperValidator:              
    def validate(self, password, user=None):
        if not any(char.isupper() for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir au moins une lettre en majuscule', code='password_no_upper'
            )
    
    def get_help_text(self):
        return 'Votre mot de passe doit contenir au moins une lettre en majuscule.'