from django.urls import path

from product.views import view_categories,view_specific_categories

urlpatterns = [
    path('categories/', view_categories, name='category-list'),
    path('categories/<int:pk>/', view_specific_categories, name='view-specific-category'),
]