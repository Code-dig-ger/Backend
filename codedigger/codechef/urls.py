from django.urls import path
from . import views

urlpatterns = [
    path('upsolve', views.CodechefUpsolveAPIView.as_view()),
    path('testing', views.testing)
]
