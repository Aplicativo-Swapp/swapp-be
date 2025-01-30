import requests
from django.conf import settings

AUTH_SERVICE_URL = settings.AUTH_SERVICE_URL

def get_user_details(user_id):
    """Busca detalhes do usuário no auth_service"""
    url = f"{AUTH_SERVICE_URL}/users/{user_id}/"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    return None
