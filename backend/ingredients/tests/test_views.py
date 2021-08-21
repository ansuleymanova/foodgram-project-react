from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ingredients.models import Ingredient

User = get_user_model()


class QueryURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Ingredient.objects.create(name='Potatoes',
                                  measurement_unit='kg')

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
        self.assertTrue(Ingredient.objects.filter(pk=1).exists())

    def test__nonexistent_tag_doesnt_exist(self):
        self.assertFalse(Ingredient.objects.filter(pk=2).exists())
