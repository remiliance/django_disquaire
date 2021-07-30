import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse

from store.models import Contact
from store.serializers import ContactSerializer


class GetAllContacts(TestCase):
    """ Test module for GET all contacts API """

    # initialize the APIClient app

    def setUp(self):
        Contact.objects.create(
            name='Casper', email='Black@hh.com')
        Contact.objects.create(
            name='Muffin', email='Brown@yahoo.com')
        Contact.objects.create(
            name='Rambo', email='BlackTT@gg.com')

    def test_get_all_contacts(self):
        client = Client()
        # get API response
        response = client.get(reverse('store:get_post_contacts'))
        # get data from db
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleContactTest(TestCase):
    """ Test module for GET single contact API """

    def setUp(self):
        self.casper = Contact.objects.create(
            name='Casper', email='Black@hh.com')
        self.muffin = Contact.objects.create(
            name='Muffin', email='Brown@yahoo.com')
        self.rambo = Contact.objects.create(
            name='Rambo', email='BlackTT@gg.com')

    def test_get_valid_single_contact(self):
        client = Client()
        response = client.get(
            reverse('store:get_delete_update_contacts', kwargs={'pk': self.rambo.pk}))
        contact = Contact.objects.get(pk=self.rambo.pk)
        serializer = ContactSerializer(contact)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_contact(self):
        client = Client()
        response = client.get(
            reverse('store:get_delete_update_contacts', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewContactTest(TestCase):
    """ Test module for inserting a new contact """

    def setUp(self):
        self.valid_payload = {
            'name': 'Muffin',
            'email': 'remilioonnnce@ooo.com'
        }
        self.invalid_payload = {
            'name': '',
            'email': 'White'
        }

    def test_create_valid_contact(self):
        client = Client()
        response = client.post(
            reverse('store:get_post_contacts'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_contact(self):
        client = Client()
        response = client.post(
            reverse('store:get_post_contacts'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleContactTest(TestCase):
    """ Test module for updating an existing contact record """

    def setUp(self):
        self.casper = Contact.objects.create(
            name='Casper', email='Black@hh.com')
        self.muffin = Contact.objects.create(
            name='Muffin', email='Brown@yahoo.com')
        self.valid_payload = {
            'name': 'Casper',
            'email': 'relou@kkk.com'
        }
        self.invalid_payload = {
            'name': '',
            'email': 'relou@kkkdd.com'
        }

    def test_valid_update_contact(self):
        client = Client()
        response = client.put(
            reverse('store:get_delete_update_contacts', kwargs={'pk': self.muffin.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_contact(self):
        client = Client()
        response = client.put(
            reverse('store:get_delete_update_contacts', kwargs={'pk': self.muffin.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleContactContact(TestCase):
    """ Test module for deleting an existing contact record """

    def setUp(self):
        self.casper = Contact.objects.create(
            name='Casper', email='Black@hh.com')
        self.muffin = Contact.objects.create(
            name='Muffin', email='Brown@yahoo.com')

    def test_valid_delete_contact(self):
        client = Client()
        response = client.delete(
            reverse('store:get_delete_update_contacts', kwargs={'pk': self.muffin.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_contact(self):
        client = Client()
        response = client.delete(
            reverse('store:get_delete_update_contacts', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
