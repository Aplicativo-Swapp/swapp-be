from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Category, PopularService
from .serializers import CategorySerializer, PopularServiceSerializer

import logging

class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class PopularServiceListView(APIView):
    def get(self, request):
        services = PopularService.objects.all()
        serializer = PopularServiceSerializer(services, many=True)
        return Response(serializer.data)
