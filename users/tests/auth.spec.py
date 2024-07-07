# org/tests/test_views.py

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('user_register')  # Adjust with your actual registration URL name

    def test_register_user_without_organisation_details(self):
        # Data for the registration payload
        user_data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'securepassword'
            # Add more fields as per your registration endpoint requirements
        }

        # Perform a POST request to register a new user
        response = self.client.post(self.register_url, user_data, format='json')

        # Assert the response status code is 201 Created (or 200 OK depending on your implementation)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the response contains the expected user details
        self.assertIn('accessToken', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['firstName'], user_data['firstName'])
        self.assertEqual(response.data['user']['email'], user_data['email'])

        # Optionally, verify default organization details (if applicable)
        # For example, you might check if the user has been assigned to a default organization
