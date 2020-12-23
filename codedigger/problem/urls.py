from django.urls import path

from .views import StatusAPIView
from . import views

urlpatterns = [
    path('', StatusAPIView.as_view()),
]
