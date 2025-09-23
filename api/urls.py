from django.urls import path, include
from rest_framework_nested import routers
from order.views import CartItemViewSet, CartViewSet, HasOrderedProduct, OrderViewSet, payment_success
from product.views import ProductImageViewSet, ProductViewSet, ReviewViewSet, CategoryViewSet
from order.views import initiate_payment, payment_success, payment_fail, payment_cancel

router = routers.DefaultRouter() # type: ignore
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet, basename='categories')
router.register('carts', CartViewSet, basename='carts')
router.register('orders', OrderViewSet, basename='orders')

product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', ReviewViewSet, basename='product-reviews')
product_router.register('images', ProductImageViewSet, basename='product-images')


cart_router=routers.NestedDefaultRouter(router,'carts',lookup='cart')
cart_router.register('items', CartItemViewSet, basename='cart-item')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls)), 
    path('', include(cart_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('payment/initiate/', initiate_payment, name='initiate-payment'),
    path('payment/success/', payment_success, name='payment-success'),
    path('payment/fail/', payment_fail, name='payment-fail'),
    path('payment/cancel/', payment_cancel, name='payment-cancel'),
    path('orders/has-ordered/<int:product_id>/', HasOrderedProduct.as_view(), name='has-ordered-product'),
]
