from django.utils.timezone import now
from rest_framework.test import APITestCase

from ..models import Mailing, Client, Message


class TestModel(APITestCase):

    def test_creates_mailings(self):
        mailing = Mailing.objects.create(date_start=now(), date_end=now(), text='Simple text',
                                         time_start=now().time(), time_end=now().time(), tag='crazy',
                                         )
        self.assertIsInstance(mailing, Mailing)
        self.assertEqual(mailing.tag, 'crazy')

    def test_creates_clients(self):
        client = Client.objects.create(phone_number='71234567890', mobile_operator_code='123',
                                       tag='crazy', timezone='UTC')
        self.assertIsInstance(client, Client)
        self.assertEqual(client.phone_number, '71234567890')

    def test_creates_messages(self):
        self.test_creates_mailings()
        self.test_creates_clients()
        message = Message.objects.create(sending_status='No sent', mailing_id=1, client_id=1)
        self.assertIsInstance(message, Message)
        self.assertEqual(message.sending_status, 'No sent')
