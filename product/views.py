from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from product.models import Product,Category
# Create your views here.
@api_view(['GET'])  
def view_specific_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        product_data = {
            "id": product.pk, 
            "name": product.name,
            "price": product.price,
            "description": product.description,
            "category": product.category.name
        }
        return Response(product_data)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)

@api_view(['GET'])
def view_categories(request):
    categories = Category.objects.all()
    category_list = [{"id": category.pk, "name": category.name} for category in categories]
    return Response({"categories": category_list})