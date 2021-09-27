from django.urls import path

from . import views

urlpatterns = [

    path('mentor', views.MentorAPIView.as_view(), name='mentor'),
    path('testing', views.testing),
]
