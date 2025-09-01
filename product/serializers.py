from rest_framework import serializers
from decimal import Decimal

from product.models import Category, Product

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

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product 
        # fields='__all__'
        fields=['id','name','price','description','category','stock','price_with_tax',]

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