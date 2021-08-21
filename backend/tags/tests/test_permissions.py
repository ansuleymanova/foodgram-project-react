import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from tags.models import Tag

User = get_user_model()


class TagPermissionTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Tag.objects.create(
            name='Dessert',
            color='000000',
            slug='dessert'
        )

    def setUp(self):
        self.user = User.objects.create_user(username='foodgram',
                                             password='foodgram')
        self.admin = User.objects.create_superuser(username='admin',
                                                   email='admin@test.com',
                                                   password='admin')
        self.guest_client = APIClient()
        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(user=self.user)
        self.admin_client = APIClient()
        self.admin_client.force_authenticate(user=self.admin)

    def test_tag_query_api_anon(self):
        response = self.guest_client.get('/api/tags/')
        self.assertEqual(response.status_code, 200)

    def test_individual_tag_api_anon(self):
        response = self.guest_client.get('/api/tags/1/')
        self.assertEqual(response.status_code, 200)

    def test_tag_query_api_auth(self):
        response = self.authorized_client.get('/api/tags/')
        self.assertEqual(response.status_code, 200)

    def test_individual_tag_api_auth(self):
        response = self.authorized_client.get('/api/tags/1/')
        self.assertEqual(response.status_code, 200)

    def test_tag_query_api_admin(self):
        response = self.admin_client.get('/api/tags/')
        self.assertEqual(response.status_code, 200)

    def test_individual_tag_api_admin(self):
        response = self.admin_client.get('/api/tags/1/')
        self.assertEqual(response.status_code, 200)

    def test_tag_post_admin(self):
        data = json.dumps({'name': 'Sauces',
                          'color': 'ffffff',
                           'slug': 'sauces'})
        response = self.admin_client.post('/api/tags/',
                                          data=data,
                                          content_type='application/json')
        self.assertEqual(response.status_code, 405)

    def test_tag_post_anon(self):
        data = json.dumps({'name': 'Sauces',
                          'color': 'ffffff',
                           'slug': 'sauces'})
        response = self.guest_client.post('/api/tags/',
                                          data=data,
                                          content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_tag_post_auth(self):
        data = json.dumps({'name': 'Sauces',
                          'color': 'ffffff',
                           'slug': 'sauces'})
        response = self.authorized_client.post('/api/tags/',
                                               data=data,
                                               content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_tag_delete_admin(self):
        response = self.admin_client.delete('/api/tags/1/')
        self.assertEqual(response.status_code, 405)

    def test_tag_delete_anon(self):
        response = self.guest_client.delete('/api/tags/1/')
        self.assertEqual(response.status_code, 401)

    def test_tag_delete_auth(self):
        response = self.authorized_client.delete('/api/tags/1/')
        self.assertEqual(response.status_code, 403)
