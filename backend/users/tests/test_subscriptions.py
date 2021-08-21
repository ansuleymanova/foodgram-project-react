from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from rest_framework.test import APIClient

from users.models import Subscription

User = get_user_model()


class QueryURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User.objects.create(username='user1',
                            password='useronepwd',
                            email='user@user.com')

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='foodgram',
                                             password='foodgram',
                                             email='foodgram@foodgram.com')
        self.admin = User.objects.create_superuser(username='admin',
                                                   email='admin@admin.com',
                                                   password='admin')
        self.guest_client = APIClient()
        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(user=self.user)
        self.admin_client = APIClient()
        self.admin_client.force_authenticate(user=self.admin)

    def test_create_subscription_response(self):
        response = self.authorized_client.get('/api/users/1/subscribe/')
        self.assertEqual(response.status_code, 201)

    def test_create_subscription_exists(self):
        self.authorized_client.get('/api/users/1/subscribe/')
        sub = Subscription.objects.get(author_id=1, subscriber_id=2)
        self.assertTrue(sub)
