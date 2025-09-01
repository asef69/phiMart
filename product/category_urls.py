from django.urls import path

from product.views import view_categories

urlpatterns = [
    path('categories/', view_categories, name='category-list')
]