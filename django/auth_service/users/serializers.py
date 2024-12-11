from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User
from django.core.files.uploadedfile import InMemoryUploadedFile

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

    def validate_profile_picture(self, value):
        """
            Validate the profile picture field.
        """
        return value

    class Meta:
        """
            Meta class to map serializer's fields with the model fields.
        """
        
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'password',
            'cpf', 'address', 'contact', 'gender', 'state', 'city',
            'profile_picture'
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

        # Handle the profile picture field specifically
        profile_picture = validated_data.pop("profile_picture", None)
        
        if profile_picture:
            # Convert InMemoryUploadedFile to bytes
            if isinstance(profile_picture, InMemoryUploadedFile):
                profile_picture.seek(0)  # Ensure the file pointer is at the beginning
                validated_data["profile_picture"] = profile_picture.read()
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance