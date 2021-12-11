from django.urls import path

from .views import *

urlpatterns = [
    path('upsolve/',
         ATUpsolveContestAPIView.as_view(),
         name='at-upsolve'),
]
