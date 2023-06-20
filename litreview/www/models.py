from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from PIL import Image


class Ticket(models.Model):
    def __str__(self):
        return f'{self.title}'
    
    title = models.CharField(max_length = 128)
    description = models.TextField(
        max_length = 2048,
        blank = True, # description can be empy
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, # CASCADE means delete all objects referenced to this user
    )
    image = models.ImageField(
        null=True, # image may not be filled in
        blank=True,
    )
    time_created = models.DateTimeField(auto_now_add=True)

    IMAGE_MAX_SIZE = (800, 800)

    def resize_image(self):
        if self.image:
            image = Image.open(self.image.path)
            image.thumbnail(self.IMAGE_MAX_SIZE)
            image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()

class Review(models.Model):
    ticket = models.ForeignKey(
        to=Ticket,
        on_delete=models.CASCADE, # CASCADE means delete all objects referenced to this ticket
    )
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),],
    )
    headline = models.CharField(max_length=128)
    body = models.TextField(
        max_length=8192,
        blank=True, # body can be empty
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, # CASCADE means delete all objects referenced to this user
    )
    time_created = models.DateTimeField(auto_now_add=True)
