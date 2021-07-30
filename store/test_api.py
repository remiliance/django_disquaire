from rest_framework.test import APITestCase
from rest_framework import status

"""
class testAPI(APITestCase):

     def test_api_contact_get_response(self):
        response = self.client.post("http://127.0.0.1:8000/store/api/contact/")
        self.assertEqual(response.satus_code, status.HTTP_200_OK)


"""

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
