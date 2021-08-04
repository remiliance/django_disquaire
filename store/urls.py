from django.conf.urls import url, include

from rest_framework import routers

from . import views, api_views  # import views so we can use them in urls.
from .api import PostContactViewSet, PostBookingViewSet
import store.receivers

app_name = 'store'

router = routers.DefaultRouter()
router.register(r'contact', PostContactViewSet)
router.register(r'booking', PostBookingViewSet)

urlpatterns = [
    #url(r'^$', views.index), # "/store" will call the method "index" in "views.py"
    url(r'^$', views.listing, name='listing'),
    url(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^search/$', views.search, name='search'),
    url(r'^api/', include(router.urls)),

    url(
        r'^api/contactapi/$',
        api_views.get_post_contacts,
        name='get_post_contacts'
    ),
    url(
        r'^api/contactapi/(?P<pk>[0-9]+)$',
        api_views.get_delete_update_contacts,
        name='get_delete_update_contacts'
    ),

]


