import django.dispatch

post_contact_move = django.dispatch.Signal(providing_args=["q"])