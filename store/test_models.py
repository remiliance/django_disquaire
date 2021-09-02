from django.test import TestCase
from store.models import Album, Contact, Artist


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


class BookingsTestCase(TestCase):
    def setUp(self):
        Contact.objects.create(name="Freddie", email="fred@queen.forever")
        Play = Album.objects.create(title="Play the game")
        Queen = Artist.objects.create(name="Queen")
        Play.artists.add(Queen)
        # art = Play.objects.filter(artists__name="Queen")

    def test_Album_artist(self):
        self.album = Album.objects.get(title='Play the game')
        self.assertEqual(self.album.title, 'Play the game')
        a = Album.objects.get(title="Play the game")
        self.assertEqual(a.artists.all().count(), 1)
        # ou
        self.assertEqual(self.album.artists.all().count(), 1)
        b = self.album.artists.all()
        result = b.first() # ici il faudrait faire un filter sur la liste plutot que de prendre le premier...
        self.assertEqual(result.name,"Queen")