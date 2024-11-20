from django.urls import reverse
from django.contrib.auth import get_user_model

from django.db import connection
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
import datetime

############################# Testing the UserRegistrationView #############################
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

############################# Testing the UserLoginView #############################
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

############################# Testing the UserLogoutView #############################
User = get_user_model()

class UserLogoutTestCase(APITestCase):
    def setUp(self):
        """
            Setup is called before each test. Creates a user to test the logout.
        """

        self.user = User.objects.create_user(
            first_name="Jhon",
            last_name="Doe",
            email="jhondoe@example.com",
            cpf="12345678901",
            password="securepassword"
        )

        self.login_url = "/api/users/login/"
        self.logout_url = "/api/users/logout/"

        # Generate tokens for the user manually
        self.tokens = RefreshToken.for_user(self.user)
        self.refresh_token = str(self.tokens)
        self.access_token = str(self.tokens.access_token)

    def test_logout_successful(self):
        """
            Test the sucessful logout invalidating the refresh token.
        """
        data = {"refresh": self.refresh_token}
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}") # Set the access token in the header
        response = self.client.post(self.logout_url, data) # Send the request with the refresh token

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Logout realizado com sucesso.")

    def test_logout_missing_refresh_token(self):
        """
            Test the logout when the refresh token is missing.
        """

        data = {} # Empty data
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}") 
        response = self.client.post(self.logout_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Refresh Token é obrigatório para logout.")

    def test_logout_invalid_refresh_token(self):
        """
            Test the logout when the refresh token is invalid.
        """
        
        data = {"refresh": "invalidtoken"} # Invalid refresh token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.post(self.logout_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Erro ao realizar logout.")

# ############################# Testing the DatabaseConnection #############################

# """
#     Test case to validate the database connection.
    
#     Run the test just to test the connection by changing settings.py

#     The database is configured only for the application, and not for testing, 
#     in this case the local database is used.

#     THAT'S WHY THIS TEST IS COMMENTED

# """

# class DatabaseConnectionTestCase(TestCase):
#     """
#         Test case to validate the database connection.
#     """

#     def test_database_connection(self):
#         """
#             Test if the database connection is successful.
#         """

#         try:
#             with connection.cursor() as cursor:
#                 cursor.execute("SELECT 1")
#                 # cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';") # Show the tables in the database to test the connection
#             print("Conexão com o banco de dados bem-sucedida!")
#         except Exception as e:
#             self.fail(f"Erro na conexão com o banco de dados: {e}")