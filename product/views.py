from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from product.models import Product,Category
from rest_framework import status
from product.serializers import ProductSerializer,CategorySerializer
from django.db.models import Count
# Create your views here.
@api_view(['GET','DELETE','PUT'])  
def view_specific_product(request, pk):
    if request.method == 'GET':
        product=get_object_or_404(Product, pk=pk)
        serializer=ProductSerializer(product)
        return Response(serializer.data)
    if request.method == 'PUT':
        product=get_object_or_404(Product, pk=pk)
        serializer=ProductSerializer(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    if request.method == 'DELETE':
        product=get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','POST'])
def view_categories(request):
    if request.method=='GET':
        categories=Category.objects.annotate(product_count=Count('products')).all()
        serializer=CategorySerializer(categories,many=True)
        return Response(serializer.data)
    if request.method=='POST':
        serializer=CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def view_products(request):
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    if request.method == 'GET':
        products = Product.objects.select_related('category').all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    


@api_view(['GET'])
def view_specific_categories(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)