from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = models.CharField(
        max_length = 20,
        unique = True,
    )
    # disabled juste to have a beautifull database with only fields needed in this project
    first_name = None
    last_name = None
    email = None
