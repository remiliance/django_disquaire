from rest_framework import viewsets
from rest_framework.response import Response

from store.models import Album, Contact, Booking, BookingLines
from store.serializers import ContactSerializer, BookingSerializer


class PostContactViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Contact to be viewed or edited.
    """

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer



class PostBookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Bookings to be viewed or edited.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
