from rest_framework import serializers

from store import models
from store.models import Album, Contact, Booking, BookingLines


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Contact
        fields = ('email', 'name')


class BookingSerializer(serializers.HyperlinkedModelSerializer):
    contact = ContactSerializer()

    class Meta:
        model = models.Booking
        fields = ('created_at', 'contacted', 'contact')
