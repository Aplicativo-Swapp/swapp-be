from django.shortcuts import render
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

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
        # logger.error("Erro na validação: %s", serializer.errors)
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
    
    def post(self, request):
        """
            Method to handle POST request for user logout.
        """
        return Response({"message": "Logout efetuado com sucesso!"}, status=status.HTTP_200_OK)   