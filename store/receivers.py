from django.dispatch import receiver

from store.models import Album, Contact
from store.signal import post_contact_move
from django.db.models.signals import post_save



@receiver(post_contact_move)
def my_callback(sender, **kwargs):
    # Faire Qqqch
    print("Contact enregistré!!!!!")
    print(kwargs['q'])


@receiver(post_save)
def my_callback(sender, **kwargs):
    if issubclass(sender, Contact):
        print("Le contact {0} a été enregistré! ".format( kwargs['instance'].id, ))