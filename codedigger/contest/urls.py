from django.urls import path

from . import views

urlpatterns = [
    path('' , views.ContestAPIView.as_view() , name = 'mentor.contest') ,
]