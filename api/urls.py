from django.urls import path, include
from rest_framework_nested import routers
from product.views import ProductViewSet, ReviewViewSet, CategoryViewSet

router = routers.DefaultRouter() # type: ignore
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet, basename='categories')

product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', ReviewViewSet, basename='product-reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls)),  # Include nested URLs
]
