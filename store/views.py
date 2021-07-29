import logging
from sqlite3 import IntegrityError
import logging as lg
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from store.forms import ContactForm
from store.models import Album, Artist, Contact, Booking, BookingLines
from django.http import HttpResponse
from django.template import Context

logging.basicConfig(level=logging.DEBUG)

def index(request):
    albums = Album.objects.filter(available=True).order_by('-created_at')[:12]
    context = {
        'albums': albums
    }
    all_albums = Album.objects.all()

    # Album.objects.create(title="Rock2")
    # Album.objects.create(title="Cat2")

    return render(request, 'store/index.html', context)

def listing(request):
    albums_list = Album.objects.filter(available=True)
    paginator = Paginator(albums_list, 3)
    page = request.GET.get('page')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        albums = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        albums = paginator.page(paginator.num_pages)
    context = {
        'albums': albums
    }
    return render(request, 'store/listing.html', context)


@transaction.atomic
def detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    artists = [artist.name for artist in album.artists.all()]
    artists_name = " ".join(artists)
    context = {
        'album_title': album.title,
        'artists_name': artists_name,
        'album_id': album.id,
        'thumbnail': album.picture
    }
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']

        try:
            with transaction.atomic():
                contact = Contact.objects.filter(email=email) # filtre ORM : Select ...where XXX = YYY
                if not contact.exists():
                    # If a contact is not registered, create a new one.
                    contact = Contact.objects.create(
                        email=email,
                        name=name
                    )
                else:
                    contact = contact.first()

                album = get_object_or_404(Album, id=album_id)
                booking1 = Booking.objects.create(
                    contact=contact,
                 #    album=album (ici = mettre booking line!)
                )

                bookingLines = BookingLines.objects.create(album=album, booking=booking1)
                album2 = bookingLines.album # test relation 1/1
                bookingLines2 = album2.bookinglines # test relation 1/1

                if album2 == album :
                    logging.debug("La fonction a bien été exécutée")
                    logging.info("Message d'information général")
                    logging.warning("Attention !")
                    logging.error("Une erreur est arrivée")
                    logging.critical("Erreur critique")
                 #   raise Warning('Allez les bleus!') ## ca marche
                    # lg.warning()

                album.available = False
                album.save()
                context = {
                    'album_title': album.title
                }
                return render(request, 'store/merci.html', context)
        except IntegrityError:
            form.errors['internal'] = "Une erreur interne est apparue. Merci de recommencer votre requête."
        # else:
        #     # Form data doesn't match the expected format.
        #     # Add errors to the template.
        #     context['errors'] = form.errors.items()
    else:
        form = ContactForm()
    context['form'] = form
    return render(request, 'store/detail.html', context)

def search(request):
    query = request.GET.get('query')
    if not query:
        albums = Album.objects.all()
    else:
        # title contains the query is and query is not sensitive to case.
        albums = Album.objects.filter(title__icontains=query)
    if not albums.exists():
        albums = Album.objects.filter(artists__name__icontains=query)
    title = "Résultats pour la requête %s"%query
    context = {
        'albums': albums,
        'title': title
    }
    return render(request, 'store/search.html', context)

def search(request):
    query = request.GET.get('query')
    if not query:
        albums = Album.objects.all()
    else:
        # title contains the query is and query is not sensitive to case.
        albums = Album.objects.filter(title__icontains=query)
    if not albums.exists():
        albums = Album.objects.filter(artists__name__icontains=query)
    title = "Résultats pour la requête %s"%query
    context = {
        'albums': albums,
        'title': title
    }
    return render(request, 'store/search.html', context)