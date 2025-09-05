from rest_framework import serializers
from order.models import Cart,CartItem
from product.models import Product
from product.serializers import ProductSerializer


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','name','price']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id'] # type: ignore
        quantity = self.validated_data['quantity'] # type: ignore

        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            self.instance = cart_item.save()
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data) # type: ignore

        return self.instance

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                f"Product with id {value} does not exists")
        return value



class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']




class CartItemSerializer(serializers.ModelSerializer):
    product=SimpleProductSerializer(read_only=True)
    total_price=serializers.SerializerMethodField(method_name='get_total_price')
    class Meta:
        model=CartItem
        fields=['id','product','quantity','total_price']

    def get_total_price(self, cart_item:CartItem):
        return cart_item.product.price * cart_item.quantity

class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(many=True, read_only=True)
    total_price=serializers.SerializerMethodField(method_name='get_total_price')
    class Meta:
        model=Cart
        fields=['id','user','items','total_price']

    def get_total_price(self, cart:Cart):
        return sum([item.product.price * item.quantity for item in cart.items.all()])     # type: ignore
    


