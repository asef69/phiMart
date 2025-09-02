from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from product.models import Product,Category, Review
from rest_framework import status
from product.serializers import ProductSerializer,CategorySerializer, ReviewSerializer
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.mixins import CreateModelMixin,UpdateModelMixin,DestroyModelMixin,ListModelMixin,RetrieveModelMixin
from django.db.models import QuerySet
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from product.filters import ProductFilter
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from product.paginations import DefaultPagination
# Create your views here.
# @api_view(['GET','DELETE','PUT'])  
# def view_specific_product(request, pk):
#     if request.method == 'GET':
#         product=get_object_or_404(Product, pk=pk)
#         serializer=ProductSerializer(product)
#         return Response(serializer.data)
#     if request.method == 'PUT':
#         product=get_object_or_404(Product, pk=pk)
#         serializer=ProductSerializer(product,data=request.data)
#         serializer.is_valid(raise_exception=True) 
#         serializer.save()
#         return Response(serializer.data)
#     if request.method == 'DELETE':
#         product=get_object_or_404(Product, pk=pk)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
# class ViewSpecificProduct(APIView):
#     def get(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    

# class ProductDetails(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.select_related('category').all()
#     serializer_class = ProductSerializer


# @api_view(['GET','POST'])
# def view_categories(request):
#     if request.method=='GET':
#         categories=Category.objects.annotate(product_count=Count('products')).all()
#         serializer=CategorySerializer(categories,many=True)
#         return Response(serializer.data)
#     if request.method=='POST':
#         serializer=CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

# class ViewCategories(APIView):
#     def get(self, request):
#         categories = Category.objects.annotate(product_count=Count('products')).all()
#         serializer = CategorySerializer(categories, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CategoryList(generics.ListAPIView):
#     queryset = Category.objects.annotate(product_count=Count('products')).all()
#     serializer_class = CategorySerializer



# @api_view(['GET','POST'])
# def view_products(request):
#     if request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     if request.method == 'GET':
#         products = Product.objects.select_related('category').all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)
    
# class ViewProducts(APIView):
#     def get(self, request):
#         products = Product.objects.select_related('category').all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    

# class ProductList(generics.ListCreateAPIView):
#     queryset = Product.objects.select_related('category').all()
#     serializer_class = ProductSerializer
    # def get_queryset(self):  # type: ignore
    #     return self.queryset
    # def get_serializer_class(self): # type: ignore
    #     return self.serializer_class
    # def get_serializer_context(self):
    #     return {'request': self.request}


# @api_view(['GET'])
# def view_specific_categories(request, pk):
#     category = get_object_or_404(Category, pk=pk)
#     serializer = CategorySerializer(category)
#     return Response(serializer.data)

# class ViewSpecificCategory(APIView):
#     def get(self, request, pk):
#         category = get_object_or_404(Category.objects.annotate(product_count=Count('products')).all(), pk=pk)
#         serializer = CategorySerializer(category)
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         category = get_object_or_404(Category.objects.annotate(product_count=Count('products')).all(), pk=pk)
#         serializer = CategorySerializer(category, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def delete(self, request, pk):
#         category = get_object_or_404(Category.objects.annotate(product_count=Count('products')).all(), pk=pk)
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class CategoryDetails(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Category.objects.annotate(product_count=Count('products')).all()
#     serializer_class = CategorySerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(product_count=Count('products')).all()
    serializer_class = CategorySerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self): # type: ignore
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'updated_at']
    ordering = ['updated_at']
    pagination_class = DefaultPagination

    # def get_queryset(self): # type: ignore
    #     queryset = Product.objects.all()
    #     category_id=self.request.query_params.get('category_id') # type: ignore
    #     if category_id is not None:
    #         queryset = Product.objects.filter(category_id=category_id)
    #     return queryset

    def destroy(self, request, *args, **kwargs):
        product=self.get_object()
        self.perform_destroy(product)
        return Response(status=status.HTTP_204_NO_CONTENT)    
