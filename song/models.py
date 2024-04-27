from django.db import models


from django.contrib.auth.models import AbstractUser, User


class Customer(models.Model):
    fullName = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    favorite_songs = models.ManyToManyField(
        'Song', related_name='favorited_by', )

    def __str__(self):
        return self.name
