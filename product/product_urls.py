from django.urls import path

from product.views import view_categories,view_specific_product

urlpatterns = [
    path('products/<int:pk>/', view_specific_product, name='product-detail'),
   
]
