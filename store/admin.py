from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.utils.safestring import mark_safe

from .models import Booking, Contact, Album, Artist, Booking, BookingLines


class BookingInline(admin.TabularInline):
    model = Booking
    fieldsets = [
        (None, {'fields': [ 'id', 'contacted', 'created_at']})
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


class BookingLinesLines(admin.TabularInline):
    model = BookingLines
    fieldsets = [
        (None, {'fields': ['album']})
    ]
    # list columns
    verbose_name = "BookingLin"
    verbose_name_plural = "BookingLiness"


@admin.register(BookingLines)
class BookingLinesAdmin(admin.ModelAdmin):
    pass

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    inlines = [BookingLinesLines, ]
    fieldsets = [
        (None, {'fields': ['contact', 'created_at']})
    ]
    list_filter = ['created_at']
    readonly_fields = ["created_at"]


    def album_link(self, booking):
        url = "/admin"
        return mark_safe("<a href='{}'>{}</a>".format(url, booking.album.title))

