from django.urls import path
from .views import CategoryListView, PopularServiceListView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('popular-services/', PopularServiceListView.as_view(), name='popular-service-list'),
]
