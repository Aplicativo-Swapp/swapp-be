from django.contrib.auth.backends import BaseBackend
from .models import User

class EmailBackend(BaseBackend):
    """
        Custom authentication backend to authenticate user by email.
    """

    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email) # Get user with email
        except User.DoesNotExist:
            return None # Return None if user is not found

        if user.check_password(password): 
            return user # Return user if password is correct

        return None # Return None if password is incorrect

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id) # Get user by id 
        except User.DoesNotExist:
            return None 