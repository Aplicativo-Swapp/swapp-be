from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
import datetime

#### Testing the UserRegistrationView
class UserRegistrationTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('register') # Get the URL of the user-register endpoint

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
            "state": "SP",
            "city": "São Paulo",
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
        self.assertEqual(user.state, self.user_data['state'])
        self.assertEqual(user.city, self.user_data['city'])

    def test_user_registration_invalid_data(self):
        incomplete_user_data = self.user_data.copy()
        incomplete_user_data.pop('email')

        # Send a POST request to the API endpoint with invalid user data
        response = self.client.post(self.url, incomplete_user_data, format='json')

        # Check that the response status code is 400 (BAD REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#### Testing the UserLoginView
User = get_user_model()

class UserLoginTestCase(APITestCase):
    def setUp(self):
        """
            Setup is called before each test. Creates a user to test the login.
        """

        self.user = User.objects.create_user(
            first_name="Jhon",
            last_name="Doe",
            email="jhondoe@example.com",
            cpf="12345678901",
            password="securepassword"
        )

        self.login_url = "/api/users/login/"

    def test_login_successful(self):
        """
            Test if the login with correct email and password returns the expected tokens.
        """

        data = {
            "email": "jhondoe@example.com",
            "password": "securepassword"
        }

        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_password(self):
        """
            Test if the login fails with an incorrect password.
        """
        
        data = {
            "email": "jhondoe@example.com",
            "password": "wrongpassword"
        }

        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Email ou Senha Inválidos")

    def test_login_invalid_email(self):
        """
            Test if the login fails with an incorrect email.
        """

        data = {
            "email": "notexist@example.com",
            "password": "securepassword"
        }

        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Email ou Senha Inválidos")

    def test_login_missing_fields(self):
        """ 
            Test if the login fails when some required field is missing.
        """

        response = self.client.post(self.login_url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Email e Senha são Obrigatórios")

    def test_login_token_generation(self):
        """
            Test if the generated tokens are valid.
        """

        data = {
            "email": "jhondoe@example.com",
            "password": "securepassword"
        }

        response = self.client.post(self.login_url, data)
        refresh_token = response.data.get("refresh")
        access_token = response.data.get("access")

        # Validate the generated tokens
        self.assertIsNotNone(refresh_token)
        self.assertIsNotNone(access_token)

        # Decode the token to check if it is valid
        token = RefreshToken(refresh_token)
        self.assertEqual(token["user_id"], self.user.id)