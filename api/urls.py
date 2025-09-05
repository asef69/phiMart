from django.urls import path, include
from rest_framework_nested import routers
from order.views import CartItemViewSet, CartViewSet
from product.views import ProductViewSet, ReviewViewSet, CategoryViewSet
    

router = routers.DefaultRouter() # type: ignore
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet, basename='categories')
router.register('carts', CartViewSet, basename='carts')

product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', ReviewViewSet, basename='product-reviews')


cart_router=routers.NestedDefaultRouter(router,'carts',lookup='cart')
cart_router.register('items', CartItemViewSet, basename='cart-item')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls)), 
    path('', include(cart_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
