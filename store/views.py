import logging
from sqlite3 import IntegrityError

from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.translation import gettext as _
from store.forms import ContactForm
from store.models import Album, Contact, Booking, BookingLines

logging.basicConfig(level=logging.DEBUG)


# @login_required
# @permission_required('catalog.can_mark_returned')
def index(request):
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    albums = Album.objects.filter(available=True).order_by('-created_at')[:12]
    context = {
        'albums': albums,
        'num_visits': num_visits
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
@login_required
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
                contact = Contact.objects.filter(email=email)  # filtre ORM : Select ...where XXX = YYY
                if not contact.exists():
                    # If a contact is not registered, create a new one.
                    contact = Contact.objects.create(
                        email=email,
                        name=name
                    )
                else:
                    contact = contact.first()
                # cr??ation du booking et de la booking line
                album = get_object_or_404(Album, id=album_id)
                booking1 = Booking.objects.create(
                    contact=contact,
                    #    album=album (ici = mettre booking line!)
                )

                bookingLines = BookingLines.objects.create(album=album, booking=booking1)
                album2 = bookingLines.album  # test relation 1/1
                bookingLines2 = album2.bookinglines  # test relation 1/1

                # juste pr tester les warnings ici
                if album2 == album:
                    logging.debug("La fonction a bien ??t?? ex??cut??e")
                    logging.info("Message d'information g??n??ral")
                    logging.warning("Attention !")
                    logging.error("Une erreur est arriv??e")
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
            form.errors['internal'] = "Une erreur interne est apparue. Merci de recommencer votre requ??te."
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
    title = "R??sultats pour la requ??te %s" % query
    context = {
        'albums': albums,
        'title': title
    }
    return render(request, 'store/search.html', context)
