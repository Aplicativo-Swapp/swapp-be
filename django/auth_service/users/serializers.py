from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone

import logging
logger = logging.getLogger(__name__)

from datetime import datetime

from drf_spectacular.utils import extend_schema_field

class UserSerializer(serializers.ModelSerializer):
    """
        Serializer to map the Model instance into JSON format. Transform the model fields into JSON. 
        Also validate the data sent to the view.
    """
    
    password = serializers.CharField(write_only=True)

    profile_picture = serializers.ImageField(
        required=False,
        write_only=True,
        help_text="Upload de imagem para o perfil do usuário."
    )

    birth_date = serializers.DateField(
        required=False,
        allow_null=True,
        help_text="Data de nascimento do usuário."
    )

    class Meta:
        """
            Meta class to map serializer's fields with the model fields.
        """
        
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'email', 'password',
            'cpf', 'address', 'contact', 'gender', 'state', 'city',
            'profile_picture', 'birth_date', 'neighborhood', 'street',
            'number', 'complement', 'zip_code', 'id_description', 'created_at',
            'updated_at', 'is_active', 'is_admin'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """
            Create and return a new user instance, given the validated data.
        """

        if User.objects.filter(email=validated_data['email']).exists():
            raise ValidationError({"email": "Este email já está em uso."})

        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user
    
    def update(self, instance, validated_data):
        """
            Update and return an existing user instance, given the validated data.
        """

        birth_date = validated_data.get("birth_date")
        if isinstance(birth_date, str):  # Check if birth_date is a string
            birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()

        # Handle the profile picture field specifically
        profile_picture = validated_data.pop("profile_picture", None)
        
        if profile_picture:
            # Convert InMemoryUploadedFile to bytes
            if isinstance(profile_picture, InMemoryUploadedFile):
                profile_picture.seek(0)  # Ensure the file pointer is at the beginning
                validated_data["profile_picture"] = profile_picture.read()
        
        # Update other fields
        for attr, value in validated_data.items():
            logger.info(f"Atualizando {attr} para {value}.")
            setattr(instance, attr, value)

        if instance.created_at and timezone.is_naive(instance.created_at):
            instance.created_at = timezone.make_aware(instance.created_at)

        if instance.date_joined and timezone.is_naive(instance.date_joined):
            instance.date_joined = timezone.make_aware(instance.date_joined)
        
        instance.birth_date = birth_date
        instance.save()
        return instance