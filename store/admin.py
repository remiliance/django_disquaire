from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Booking, Contact, Album, Artist, Booking


class BookingInline(admin.TabularInline):
    model = Booking
    fieldsets = [
        (None, {'fields': ['album', 'contacted', 'created_at']})
    ]
    readonly_fields = ["created_at"]
    # list columns
    verbose_name = "Réservation"
    verbose_name_plural = "Réservations"


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    inlines = [BookingInline, ]  # list of bookings made by a contact


class AlbumArtistInline(admin.TabularInline):
    model = Album.artists.through # the query goes through an intermediate table.


@admin.register(Album)
class ContactAdmin(admin.ModelAdmin):
    inlines = [AlbumArtistInline, ]  # list of artist
    search_fields = ['reference', 'title']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_filter = ['created_at', 'contacted']
    readonly_fields = ["created_at", "contact", 'album_link', 'contacted']

    def album_link(self, booking):
        url = "/admin"
        return mark_safe("<a href='{}'>{}</a>".format(url, booking.album.title))