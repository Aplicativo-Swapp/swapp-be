import requests
from django.conf import settings

from rest_framework_simplejwt.tokens import RefreshToken

AUTH_SERVICE_URL = settings.AUTH_SERVICE_URL  # Exemplo: http://auth-service:8001/api

def get_user_details(user_id):
    """
        Search for user details in the auth_service
    """
    url = f"{AUTH_SERVICE_URL}/users/{user_id}/"
    headers = {"Authorization": f"Bearer {get_auth_token()}"}

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    return None

def get_auth_token():
    """
        Get the token of the authenticated user (if necessary for the service)
    """
    
    refresh_token = RefreshToken(settings.SIMPLE_JWT["REFRESH_TOKEN"])
    return str(refresh_token.access_token)


