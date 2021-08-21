from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from tags.models import Tag

User = get_user_model()


class QueryURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Tag.objects.create(
            name='Dessert',
            color='000000',
            slug='dessert'
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='foodgram')
        self.admin = User.objects.create_superuser('admin',
                                                   'admin@test.com',
                                                   'admin')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.admin_client = Client()
        self.admin_client.force_login(self.admin)

    def test_tag_exists(self):
        self.assertTrue(Tag.objects.filter(pk=1).exists())

    def test__nonexistent_tag_doesnt_exist(self):
        self.assertFalse(Tag.objects.filter(pk=2).exists())
