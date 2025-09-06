from rest_framework import serializers
from order.models import Cart,CartItem, Order, OrderItem
from order.services import OrderService
from product.models import Product
from product.serializers import ProductSerializer



class EmptySerializer(serializers.Serializer):
    pass


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
        read_only_fields = ['user']

    def get_total_price(self, cart:Cart):
        return sum([item.product.price * item.quantity for item in cart.items.all()])     # type: ignore
    

class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'total_price']  



class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total_price', 'created_at', 'items']
        read_only_fields = ['user', 'status', 'total_price', 'created_at']

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, value):
        if not Cart.objects.filter(pk=value).exists():
            raise serializers.ValidationError("No cart with the given id exists")
        if not CartItem.objects.filter(cart_id=value).exists():
            raise serializers.ValidationError("The cart is empty")
        return value

    def create(self, validated_data):
        cart_id = validated_data['cart_id']
        user_id = self.context['user_id']
        try:
            order = OrderService.create_order(user_id, cart_id)
            return order
        except ValueError as e:
            raise serializers.ValidationError(str(e))
    def to_representation(self, instance): # type: ignore
        return OrderSerializer(instance).data
    

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']   

    # def update(self, instance, validated_data):
    #     new_status=validated_data['status']
    #     if new_status == Order.CANCELED:
    #         return OrderService.cancel_order(instance, self.context['user'])
    #     if not self.context['user'].is_staff:
    #         raise serializers.ValidationError({"detail":"Only admin users can update the order status."})
    #     return super().update(instance, validated_data)