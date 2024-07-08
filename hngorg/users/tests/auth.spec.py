
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from org.models import Organisation

class UserRegistrationTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('user_register')
        self.login_url = reverse('user_login')

    def test_register_user_with_default_organisation(self):
        data = {
            'firstName': 'Johnny',
            'lastName': 'john',
            'email': 'john@gmail.com',
            'password': 'password123',
          
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get()
        self.assertEqual(user.organisations.name, "John's Organisation")
        self.assertEqual(response.data['email'], 'john@example.com')
        self.assertIn('token', response.data)  

    def test_login_user_successfully(self):
        user = User.objects.create_user(firstName= 'ac', lastName = 'jh', email='john@example.com', password='password123', )
        data = {
            'email': 'john@example.com',
            'password': 'password123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'john@example.com')
        self.assertIn('token', response.data) 

    def test_register_user_with_missing_fields(self):
        data = {
            'username': 'john_doe'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertIn('email', response.data)
        self.assertIn('firstName', response.data)
        self.assertIn('lastName', response.data)

    def test_register_user_with_duplicate_email(self):
        User.objects.create_user(firstName= 'ac', lastName = 'jh', email='john@example.com', password='password123', )
        data = {
            'first_name': 'john',
            'last_name': 'johnny',
            'email': 'john@example.com',
            'password': 'password123',
            
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)