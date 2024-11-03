from rest_framework import serializers
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
            'first_name', 'last_name', 'cpf', 'email', 'password',
            'address', 'contact', 'gender', 'birth_date'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """
            Create and return a new user instance, given the validated data.
        """

        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user