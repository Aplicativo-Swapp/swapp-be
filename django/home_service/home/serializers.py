from rest_framework import serializers
from .models import Category, PopularService

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon']


class PopularServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopularService
        fields = ['id', 'title', 'location', 'rating', 'reviews_count', 'image']
