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
class Song(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    album = models.CharField(max_length=200, null=True, blank=True)
    artist = models.CharField(max_length=200)
    duration = models.IntegerField(null=True, blank=True)
    release_date = models.DateField(blank=True, null=True, default=None)
    created_at = models.DateField(
        auto_now_add=True)
    song_file = models.FileField(
        upload_to='songs/', default=None, null=True, blank=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='songs', null=True, blank=True)
    def __str__(self):
        return self.title


class Playlist(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    customer = models.ForeignKey(
        Customer, default="", blank=True, null=True, on_delete=models.CASCADE)
    song = models.ManyToManyField(
        Song, related_name="playlist", blank=True)
    image = models.FileField(
        upload_to='images/', default=None, null=True, blank=True)

    def __str__(self):
        return self.name
