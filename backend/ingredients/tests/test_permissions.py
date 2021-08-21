import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from ingredients.models import Ingredient

User = get_user_model()


class IngredientPermissionTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Ingredient.objects.create(name='Potatoes',
                                  measurement_unit='kg')

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

    def test_ingredient_query_api_anon(self):
        response = self.guest_client.get('/api/ingredients/')
        self.assertEqual(response.status_code, 200)

    def test_individual_ingredient_api_anon(self):
        response = self.guest_client.get('/api/ingredients/1/')
        self.assertEqual(response.status_code, 200)

    def test_ingredient_query_api_auth(self):
        response = self.authorized_client.get('/api/ingredients/')
        self.assertEqual(response.status_code, 200)

    def test_individual_ingredient_api_auth(self):
        response = self.authorized_client.get('/api/ingredients/1/')
        self.assertEqual(response.status_code, 200)

    def test_ingredient_query_api_admin(self):
        response = self.admin_client.get('/api/ingredients/')
        self.assertEqual(response.status_code, 200)

    def test_individual_ingredient_api_admin(self):
        response = self.admin_client.get('/api/ingredients/1/')
        self.assertEqual(response.status_code, 200)

    def test_ingredient_post_admin(self):
        data = json.dumps({'name': 'Cupcakes',
                           'measurement_unit': 'pc'})
        response = self.admin_client.post('/api/ingredients/',
                                          data=data,
                                          content_type='application/json')
        self.assertEqual(response.status_code, 405)

    def test_ingredient_post_anon(self):
        data = json.dumps({'name': 'Cupcakes',
                           'measurement_unit': 'pc'})
        response = self.guest_client.post('/api/ingredients/',
                                          data=data,
                                          content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_ingredient_post_auth(self):
        data = json.dumps({'name': 'Cupcakes',
                           'measurement_unit': 'pc'})
        response = self.authorized_client.post('/api/ingredients/',
                                               data=data,
                                               content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_ingredient_delete_admin(self):
        response = self.admin_client.delete('/api/ingredients/1/')
        self.assertEqual(response.status_code, 405)

    def test_ingredient_delete_anon(self):
        response = self.guest_client.delete('/api/ingredients/1/')
        self.assertEqual(response.status_code, 401)

    def test_ingredient_delete_auth(self):
        response = self.authorized_client.delete('/api/ingredients/1/')
        self.assertEqual(response.status_code, 403)
