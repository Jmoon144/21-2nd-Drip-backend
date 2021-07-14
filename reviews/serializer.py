# from products.views import ProductsAPIView
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Review

class ReviewSerializer(ModelSerializer):
    
    class Meta:
        model = Review
        fields = ('id', 'created_at', 'content', 'rating', 'image_url', 'product', 'user')

    # def get_like_count(self, request):

    # def review_count
    # def like
    # def user_image
    # def avgrating