from rest_framework import serializers
from decimal import Decimal

from phi_mart import settings
from product.models import Category, Product, ProductImage, Review
from django.contrib.auth import get_user_model

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description','product_count']
    product_count = serializers.IntegerField(source='products.count', read_only=True)


# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField(max_length=255)
#     unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, source='price')
#     price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
#     description = serializers.CharField(max_length=1000)
#     #category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category.id')
#     #category=serializers.StringRelatedField()
#     #category=CategorySerializer()
#     category=serializers.HyperlinkedRelatedField(
#         queryset=Category.objects.all(),
#         view_name='view-specific-category',

#     )
#     def calculate_tax(self, product):
#         price = product.price
#         return round(price * Decimal(1.1), 2)
class ProductImageSerializer(serializers.ModelSerializer):
    image=serializers.ImageField()
    class Meta:
        model=ProductImage
        fields=['id','image']
class ProductSerializer(serializers.ModelSerializer):
    images=ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model=Product 
        # fields='__all__'
        fields=['id','name','price','description','category','stock','price_with_tax','images']

    price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax')
    
    def calculate_tax(self, product):
        price = product.price
        return round(price * Decimal(1.1), 2)

    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError("Price must be a positive number.")
        return price

    # def create(self, validated_data):
    #     product=Product(**validated_data)
    #     product.save()
    #     return product

class ReviewSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField(method_name='get_user')
    class Meta:
        model = Review
        fields = ['id', 'user', 'comment', 'ratings', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def create(self, validated_data):
        product_id=self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
    
    def get_user(self, obj):
        return SimpleUserSerializer(obj.user).data
    

class SimpleUserSerializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField(method_name='get_current_user_name')
    class Meta:
        model = get_user_model()
        fields = ['id', 'name', 'email']    

        def get_current_user_name(self,obj):
            return obj.get_full_name()
        




       
