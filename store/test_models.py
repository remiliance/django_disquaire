from django.test import TestCase
from django.test import RequestFactory
from store.models import Album, Contact

# test data creation
class AlbumTestCase(TestCase):
        def setUp(self):
          Album.objects.create(title="Rock")
          Album.objects.create(title="Cat")

        def test_Album(self):
          rock_album = Album.objects.get(title="Rock")
          cat_album = Album.objects.get(title="Cat")
          self.assertEqual(rock_album.__str__(), 'Rock')
          self.assertEqual(cat_album.title, 'Cat')

