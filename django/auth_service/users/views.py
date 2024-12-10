from django.shortcuts import render
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .serializers import UserSerializer
from .models import User

import logging
logger = logging.getLogger(__name__)

class UserRegistrationView(APIView):
    """
        Class to handle user registration.
    """
    
    def post(self, request, *args, **kwargs):
        """
            Method to handle POST request for user registration.
        """
        
        logger.debug("Dados recebidos: %s", request.data)
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Usuário criado com sucesso!"}, status=201)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Erro na validação: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    """
        Class to handle user login.
    """
    
    def post(self, request):
        """
            Method to handle POST request for user login.
        """

        logger.debug("Dados recebidos: %s", request.data)

        # Check if email and password are provided in the request
        if 'email' not in request.data or 'password' not in request.data:
            raise AuthenticationFailed("Email e Senha são Obrigatórios")

        # Taking the email and password from the request
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate user with email and password
        user = authenticate(email=email, password=password)
        
        if user is None:  # Check if user is authenticated
            raise AuthenticationFailed("Email ou Senha Inválidos")

        # Generate tokens JWT for the user and return them 
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': "Login efetuado com sucesso!"
            }, status=status.HTTP_200_OK)
    
class UserLogoutView(APIView):
    """
        Class to handle user logout.
    """
    
    permission_classes = [IsAuthenticated] # Only authenticated users can logout

    def post(self, request, *args, **kwargs):
        """
            Method to handle POST request for user logout.
        """
        try:
            # Recover the refresh token from the request body
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"detail": "Refresh Token é obrigatório para logout."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            # Invalidate the refresh token
            token = RefreshToken(refresh_token)  
            token.blacklist()  # Add the token to the blacklist of tokens (revocation list)

            return Response({"detail": "Logout realizado com sucesso."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": "Erro ao realizar logout."}, status=status.HTTP_400_BAD_REQUEST)
        
class UserUpdateView(APIView):
    """
        Class to handle user update.
    """

    permission_classes = [IsAuthenticated] # Only authenticated users can update their profile
    parser_classes = [MultiPartParser, FormParser, JSONParser]  # Allow file uploads
    
    def put(self, request, *args, **kwargs):
        """
            Handle PUT request to update user profile.
        """
        user = request.user

        # Handle JSON data (e.g., from tests)
        if isinstance(request.data, dict):
            data = request.data
        else:
            # Convert multipart data to dictionary
            data = {key: request.data[key] for key in request.data}

        serializer = UserSerializer(user, data=data, partial=True)  # Allow partial updates
        
        if serializer.is_valid():
            serializer.save()

            send_mail(
                subject="Perfil Atualizado",
                message=f"Olá {user.first_name}, seu perfil foi atualizado com sucesso!",
                from_email="no-reply@swapp.com",
                recipient_list=[user.email],
                fail_silently=False,
            )

            logger.info(f"Usuário {user.email} atualizado com sucesso.")
            return Response({"message": "Perfil atualizado com sucesso!"}, status=status.HTTP_200_OK)
        
        logger.error(f"Falha ao atualizar usuário {user.email}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDeleteView(APIView):
    """
        Class to handle user account deletion.
    """
    
    permission_classes = [IsAuthenticated]  # Require authentication

    def delete(self, request, *args, **kwargs):
        """
            Handle DELETE request to delete user account.
        """
        user = request.user
        user_email = user.email

        try:
            user.delete()
            logger.info(f"User {user_email} deleted successfully.")
            return Response({"message": "Usuário deletado com sucesso!"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Error deleting user {user_email}: {e}")
            return Response({"error": "Erro ao deletar o usuário."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)