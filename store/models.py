import importlib

from django.db import models
from store.signal import *

class Artist(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    email = models.EmailField(max_length=100)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    # utiliser pour le signal
    def move(self, quantity):
        post_contact_move.send(sender=self, q=quantity)

class Album(models.Model):
    reference = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)
    title = models.CharField(max_length=200)
    picture = models.URLField()
    artists = models.ManyToManyField(Artist, related_name='albums', blank=True)

    reference = models.IntegerField('référenceahah', blank=True, null=True)
    class Meta:
        verbose_name = "album"
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return self.title

    """"@classmethod
    def create(cls, title):
            album = cls(title=title)
            # do something with the book
            return album
    """


class Booking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    contacted = models.BooleanField(default=False)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

    def __str__(self):
        return self.contact.name


class BookingLines(models.Model):
    album = models.OneToOneField(Album, on_delete=models.DO_NOTHING)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)


    def __str__(self):
        return str(self.booking.id)


"""
ARTISTS = {
  'francis-cabrel': {'name': 'Francis Cabrel'},
  'lej': {'name': 'Elijay'},
  'rosana': {'name': 'Rosana'},
  'maria-dolores-pradera': {'name': 'María Dolores Pradera'},
}


ALBUMS = [
  {'name': 'Sarbacane', 'artists': [ARTISTS['francis-cabrel']]},
  {'name': 'La Dalle', 'artists': [ARTISTS['lej']]},
  {'name': 'Luna Nueva', 'artists': [ARTISTS['rosana'], ARTISTS['maria-dolores-pradera']]}
]
"""
