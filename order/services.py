from order.models import Cart, CartItem, OrderItem, Order
from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError


class OrderService:
    @staticmethod
    def create_order(user_id, cart_id):
        with transaction.atomic():
            cart = Cart.objects.get(pk=cart_id)
            cart_items = cart.items.select_related('product').all() # type: ignore

            total_price = sum([item.product.price *
                               item.quantity for item in cart_items])

            order = Order.objects.create(
                user_id=user_id, total_price=total_price)

            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity,
                    total_price=item.product.price * item.quantity
                )
                for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)

            cart.delete()

            return order

    @staticmethod
    def cancel_order(order,user):
        if order.user != user and not user.is_staff:
            raise PermissionDenied({"detail": "You do not have permission to cancel this order."})
        
        if order.status in [Order.SHIPPED, Order.DELIVERED, Order.CANCELED]:
            raise ValidationError({"detail": f"Cannot cancel an order that is {order.status}."})

        order.status = Order.CANCELED
        order.save()
        return order
