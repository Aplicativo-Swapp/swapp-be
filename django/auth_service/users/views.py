from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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