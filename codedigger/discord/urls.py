from django.urls import path

from .views import *

urlpatterns = [path('verify', VerifyView.as_view(), name="verify-discord")]
