from django.urls import path
from . import views

urlpatterns = [
    path('upsolve/<str:username>', views.CodechefUpsolveAPIView.as_view()),
    path('recentsub/<str:username>', views.CodechefRecentSubmissionAPIView.as_view()),
    path('testing', views.testing)
]
