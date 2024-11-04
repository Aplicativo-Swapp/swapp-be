from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User
import datetime


# Testing the UserRegistrationView
class UserRegistrationTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('user-register') # Get the URL of the user-register endpoint

        # Define valid user data
        self.user_data = {
            "first_name": "Luiz",
            "last_name": "Moloni",
            "cpf": "12345678901",
            "email": "luiz.moloni@example.com",
            "password": "senhaSegura123",
            "address": "Rua Exemplo, 123",
            "contact": "11987654321",
            "gender": "Masculino",
            "birth_date": "2003-05-03"
        }

    def test_user_registration(self):
        # Send a POST request to the API endpoint with valid user data
        response = self.client.post(self.url, self.user_data, format='json')

        # Check that the response status code is 201 (CREATED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the user was created
        # self.assertEqual(User.objects.count(), 1)

        # Check that the user was created with the correct data
        user = User.objects.get(email=self.user_data['email'])
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])   
        self.assertEqual(user.cpf, self.user_data['cpf'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password'])) # Check that the password was criptographed
        self.assertEqual(user.address, self.user_data['address'])
        self.assertEqual(user.contact, self.user_data['contact'])
        self.assertEqual(user.gender, self.user_data['gender'])
        self.assertEqual(user.birth_date, datetime.date.fromisoformat(self.user_data['birth_date']))

    def test_user_registration_invalid_data(self):
        incomplete_user_data = self.user_data.copy()
        incomplete_user_data.pop('email')

        # Send a POST request to the API endpoint with invalid user data
        response = self.client.post(self.url, incomplete_user_data, format='json')

        # Check that the response status code is 400 (BAD REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
