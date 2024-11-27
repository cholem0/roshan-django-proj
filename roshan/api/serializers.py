from rest_framework import serializers
from .models import Category , Product , Cart , CartItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id' , 'name']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id' , 'name' , 'price' , 'visits' , 'category']

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.IntegerField(source='product.price', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity']

    def create(self, validated_data):
        #quantity bug , hard coded to 1
        validated_data['quantity'] = 1
        return super().create(validated_data)
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items']

