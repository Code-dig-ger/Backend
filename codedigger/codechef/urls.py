from django.urls import path
from . import views

urlpatterns = [
    path('upsolve', views.CodechefUpsolveAPIView.as_view(), name="codechef-upsolve"),
    path('testing', views.testing)
]
