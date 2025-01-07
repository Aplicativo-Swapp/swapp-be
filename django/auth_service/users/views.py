from django.shortcuts import render
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.models import update_last_login

from users.tasks import send_user_update_email, send_user_delete_email, send_user_change_password_email, send_user_register_email

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

from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

class UserRegistrationView(APIView):
    """
        Class to handle user registration.
    """

    @extend_schema(
        summary="Register a new user",
        description="Endpoint to register a new user by providing necessary details like email, password, and personal information.",
        request=UserSerializer,
        responses={
            201: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT
        },
        examples=[
            OpenApiExample(
                "Successful Registration",
                description="Example of a successful user registration.",
                value={
                    "message": "Usuário criado com sucesso!"
                },
                response_only=True,
            ),
            OpenApiExample(
                "Validation Error",
                description="Example of validation error when invalid data is provided.",
                value={
                    "email": ["Este campo é obrigatório."],
                    "password": ["Este campo é obrigatório."]
                },
                response_only=True,
            )
        ]
    )
    
    def post(self, request, *args, **kwargs):
        """
            Method to handle POST request for user registration.
        """
        
        logger.debug("Dados recebidos: %s", request.data)
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            # Send email notification to the user
            send_user_register_email.delay(serializer.data['first_name'], serializer.data['email'])

            return Response({"message": "Usuário criado com sucesso!"}, status=201)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Erro na validação: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    """
        Class to handle user login.
    """

    @extend_schema(
        summary="User Login",
        description="Authenticate a user by email and password and return JWT tokens.",
        request=OpenApiTypes.OBJECT,
        parameters=[
            OpenApiParameter("email", OpenApiTypes.EMAIL, description="The email of the user."),
            OpenApiParameter("password", OpenApiTypes.STR, description="The password of the user."),
        ],
        responses={
            200: OpenApiExample(
                "Login bem-sucedido",
                value={
                    "refresh": "jwt-refresh-token",
                    "access": "jwt-access-token",
                    "message": "Login efetuado com sucesso!",
                },
            ),
            401: "Credenciais inválidas.",
        },
    )
    
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

    @extend_schema(
        summary="User Logout",
        description="Logout a user by providing their refresh token.",
        request=OpenApiTypes.OBJECT,
        parameters=[
            OpenApiParameter("refresh", OpenApiTypes.STR, description="The refresh token of the user."),
        ],
        responses={
            200: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT
        },
        examples=[
            OpenApiExample(
                "Successful Logout",
                description="Example of a successful user logout.",
                value={
                    "detail": "Logout realizado com sucesso."
                },
                response_only=True,
            ),
            OpenApiExample(
                "Invalid Refresh Token",
                description="Example of an invalid refresh token.",
                value={
                    "detail": "Erro ao realizar logout."
                },
                response_only=True,
            )
        ]
    )

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
    
    @extend_schema(
        summary="Update user profile",
        description="Endpoint to update user details, including profile picture.",
        request=UserSerializer,
        responses={
            200: OpenApiExample(
                "Success Response",
                value={"message": "Perfil atualizado com sucesso!"},
                status_codes=["200"],
            ),
            400: OpenApiExample(
                "Validation Error",
                value={"email": ["Este email já está em uso."]},
                status_codes=["400"],
            ),
        },
        examples=[
            OpenApiExample(
                "Exemplo de Requisição",
                value={
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "john.doe@example.com",
                    "address": "Rua Nova, 123",
                    "profile_picture": "(arquivo de imagem)"
                },
                request_only=True,
            ),
        ],
    )

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

        logger.info(f"Dados recebidos para atualização do perfil: {data}")

        serializer = UserSerializer(user, data=data, partial=True)  # Allow partial updates
        
        if serializer.is_valid():
            serializer.save()
            
            # Send email notification to the user
            send_user_update_email.delay(user.first_name, user.email)

            # try:
            #     send_mail(
            #         subject="Perfil Atualizado",
            #         message=f"Olá {user.first_name},\n\nSeu perfil foi atualizado com sucesso!\n\nEquipe SwApp",
            #         from_email="no-reply@swapp.com",
            #         recipient_list=[user.email],
            #         fail_silently=False,
            #     )
            #     logger.info(f"Notificação de atualização enviada para {user.email}.")
            # except Exception as e:
            #     logger.error(f"Erro ao enviar e-mail para {user.email}: {e}")

            logger.info(f"Usuário {user.email} atualizado com sucesso.")
            return Response({"message": "Perfil atualizado com sucesso!"}, status=status.HTTP_200_OK)
        
        logger.error(f"Falha ao atualizar usuário {user.email}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDeleteView(APIView):
    """
        Class to handle user account deletion.
    """
    
    permission_classes = [IsAuthenticated]  # Require authentication

    @extend_schema(
        summary="Delete user account",
        description="Endpoint to delete user account.",
        responses={
            204: OpenApiTypes.OBJECT,
            500: OpenApiTypes.OBJECT
        },
    )

    def delete(self, request, *args, **kwargs):
        """
            Handle DELETE request to delete user account.
        """
        user = request.user
        user_email = user.email

        try:
            user.delete()

            # Send email notification to the user
            send_user_delete_email.delay(user.first_name, user_email)

            logger.info(f"User {user_email} deleted successfully.")
            return Response({"message": "Usuário deletado com sucesso!"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Error deleting user {user_email}: {e}")
            return Response({"error": "Erro ao deletar o usuário."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UserDetailView(APIView):
    """
        Class to retrieve user details for editing the profile.
    """

    permission_classes = [IsAuthenticated]  # Require authentication

    @extend_schema(
        summary="Retrieve user details",
        description="Endpoint to fetch user details to edit the profile.",
        responses={
            200: UserSerializer,
            401: OpenApiExample(
                "Unauthorized Access",
                value={"detail": "As credenciais de autenticação não foram fornecidas."},
                response_only=True,
            ),
        },
    )

    def get(self, request, *args, **kwargs):
        """
            Handle GET request to retrieve user details.
        """
        user = request.user  # Get the authenticated user
        serializer = UserSerializer(user)  # Serialize user instance
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
    """
        Class to change user password.
    """

    permission_classes = [IsAuthenticated]  # Require authentication

    @extend_schema(
        summary="Change user password",
        description="Endpoint to change user password.",
        request=UserSerializer,
        responses={
            200: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
            401: OpenApiTypes.OBJECT,
        },
    )
    
    def put(self, request, *args, **kwargs):
        """
            Handle PUT request to change user password.
        """

        user = request.user  # Get the authenticated user
        data = request.data  # Get the request data

        current_password = data.get("currentPassword")
        new_password = data.get("newPassword")
        confirm_new_password = data.get("confirmNewPassword")

        if not current_password or not new_password or not confirm_new_password: # Check if all fields are provided
            return Response(
                {"message": "Todos os campos são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(current_password): # Check if current password is correct
            return Response(
                {"message": "Senha atual incorreta."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_password != confirm_new_password: # Check if new password and confirm new password are the same
            return Response(
                {"message": "As novas senhas não coincidem."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)  # Set the new password
        user.save()  # Save the user
        send_user_change_password_email.delay(user.first_name, user.email) # Send email notification to the user
        update_last_login(None, user)  # Update last login

        return Response(
            {"message": "Senha alterada com sucesso!"},
            status=status.HTTP_200_OK
        )