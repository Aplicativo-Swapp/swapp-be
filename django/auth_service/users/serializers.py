from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
        Serializer to map the Model instance into JSON format. Transform the model fields into JSON. 
        Also validate the data sent to the view.
    """
    
    password = serializers.CharField(write_only=True)

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