from django.urls import path
from .views import UserView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
]