from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Mailing, Message, Client


class TestStat(APITestCase):

    def test_mailing(self):
        mail_count = Mailing.objects.all().count()
        mail_create = {"date_start": now(), "date_end": now(), 'time_start': now().time(),
                       'time_end': now().time(), "text": "Simple text", "tag": "crazy",
                       "mobile_operator_code": '412'}
        response = self.client.post('http://127.0.0.1:8000/api/mailings/', mail_create)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Mailing.objects.all().count(), mail_count + 1)
        self.assertEqual(response.data['text'], 'Simple text')
        self.assertIsInstance(response.data['text'], str)

    def test_client(self):
        client_count = Client.objects.all().count()
        client_create = {"phone_number": '79999999999',
                         "tag": "crazy", "timezone": "UTC"}
        response = self.client.post('http://127.0.0.1:8000/api/clients/', client_create)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.all().count(), client_count + 1)
        self.assertEqual(response.data['phone_number'], '79999999999')
        self.assertIsInstance(response.data['phone_number'], str)

    def test_message(self):
        response = self.client.get('http://127.0.0.1:8000/api/messages/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stat(self):
        self.test_mailing()
        url = 'http://127.0.0.1:8000/api/mailings'
        response = self.client.get(f'{url}/1/info/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(f'{url}/2/info/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.get(f'{url}/fullinfo/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Total number of mailings'], 1)
        self.assertIsInstance(response.data['Total number of mailings'], int)
        self.assertIsInstance(response.data['The number of messages sent'], dict)
