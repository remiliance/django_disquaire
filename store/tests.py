from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from store.models import Album, Artist, Contact, Booking


# Index page
# test that index page returns a 200
class IndexPageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class DetailPageTestCase(TestCase):
    # ran before each test.
    def setUp(self):
        impossible = Album.objects.create(title="Transmission Impossible")
        self.album = Album.objects.get(title='Transmission Impossible')

    # test that detail page returns a 200 if the item exists
    def test_detail_page_returns_200(self):
        album_id = self.album.id
        response = self.client.get(reverse('store:detail', args=(album_id,)))
        self.assertEqual(response.status_code, 200)

    # test that detail page returns a 404 if the item does not exist
    def test_detail_page_returns_404(self):
        album_id = self.album.id + 1
        response = self.client.get(reverse('store:detail', args=(album_id,)))
        self.assertEqual(response.status_code, 404)


class BookingPageTestCase(TestCase):

    def setUp(self):
        Contact.objects.create(name="Freddie", email="fred@queen.forever")
        impossible = Album.objects.create(title="Transmission Impossible")
        journey2 = Artist.objects.create(name="Jour")
        impossible.artists.add(journey2)
        self.album = Album.objects.get(title='Transmission Impossible')
        self.contact = Contact.objects.get(name='Freddie')

        # test that a new booking is made

    def test_new_booking_is_registered(self):
        old_bookings = Booking.objects.count()
        album_id = self.album.id
        name = self.contact.name
        email = self.contact.email
        response = self.client.post(reverse('store:detail', args=(album_id,)), {
            'name': name,
            'email': email
        })
        counter = Booking.objects.count()
        self.assertEqual(counter, old_bookings + 1) # Création du booking via le formulaire client

        # test that a booking belongs to a contact


""" cassé car plus d'album rattaché à un booking mais un booking line
    def test_new_booking_belongs_to_a_contact(self):
        album_id = self.album.id
        name = self.contact.name
        email = self.contact.email
        response = self.client.post(reverse('store:detail', args=(album_id,)), {
            'name': name,
            'email': email
        })
        booking = Booking.objects.first()
        self.assertEqual(self.contact, booking.contact)
"""


# test that a booking belong to an album
# idem

# test that list return the full list of albums
class GetAllAlbumList(TestCase):
    """ Test module for GET all puppies API """

    def setUp(self):
        Album.objects.create(title="Rock")
        Album.objects.create(title="Cat")
        Album.objects.create(title="Paul")

    def test_get_all_albums(self):
        # get API response
        response = self.client.get(reverse('store:listing'))
        counter = Album.objects.count()
        print(counter)
        self.assertEqual(counter, 3)
        self.assertEqual(response.status_code, 200)
