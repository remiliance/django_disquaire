import unittest
from django.test import Client

class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get('/')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the rendered context contains 5 customers.
        self.assertEqual(len(response.context['albums']), 5) # test que l'on a bien 5 albums en db au lancement