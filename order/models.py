from django.db import models
from users.models import User
from product.models import Product
from uuid import uuid4
from django.core.validators import MinValueValidator
# Create your models here.
class Cart(models.Model):
    id=models.UUIDField(primary_key=True, editable=False,default=uuid4)
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.first_name} {self.user.last_name}" 
    
class CartItem(models.Model):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = [['cart', 'product']]

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in cart of {self.cart.user.first_name} {self.cart.user.last_name}"



class Order(models.Model):
    PENDING='pending'
    SHIPPED='shipped'
    DELIVERED='delivered'
    STATUS_CHOICES=[
        (PENDING,'Pending'),
        (SHIPPED,'Shipped'),
        (DELIVERED,'Delivered'),
    ]
    status=models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price=models.DecimalField(max_digits=10, decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def __str__(self) :
        return f"Order {self.id} of {self.user.username} - {self.status}" # type: ignore
    


class OrderItem(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    price=models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) :
        return f"{self.quantity} of {self.product.name} - {self.price}"
