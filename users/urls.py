from django.urls import path
from .views import ActivateUserView

urlpatterns = [
    path('activate/<uid>/<token>/', ActivateUserView.as_view(), name='activate'),
]
