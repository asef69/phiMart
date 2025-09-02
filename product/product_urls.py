from django.urls import path

from product.views import  ProductViewSet,ReviewViewSet

urlpatterns = [
    path('<int:pk>/', ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='product-detail'),
    path('', ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='product-list'),
    path('<int:pk>/reviews/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'}), name='product-review-list'),
    path('<int:pk>/reviews/<int:review_pk>/', ReviewViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='product-review-detail'),
]
