from django.urls import path

from . import views

urlpatterns = [
    path('search/', views.SearchUser.as_view()),
    path('mentor', views.MentorAPIView.as_view(), name='mentor'),
    path('testing', views.testing),
    
]
