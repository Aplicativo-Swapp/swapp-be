from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView, UserUpdateView, UserDeleteView

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('user/update/', UserUpdateView.as_view(), name='user-update'),
    path('user/delete/', UserDeleteView.as_view(), name='user-delete'),
]