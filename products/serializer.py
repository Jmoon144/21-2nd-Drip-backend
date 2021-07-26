# from products.views import ProductsAPIView
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Product


class ProductSerializer(ModelSerializer):
    avg_score = serializers.ReadOnlyField()
    new       = serializers.ReadOnlyField()
    hot       = serializers.ReadOnlyField()
    discount  = serializers.ReadOnlyField()
    # address   = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ('id', 'name', 'address', 'price', 'discount', 'main_image', 'sell_count', 'avg_score', 'date', 'new', 'hot','check')

    # def get_address(self, object):
    #     return object.address.split()[0]