from django.urls import path
from . import views

urlpatterns = [
    # path('testing', views.testing),
    # path('userdata/<handle>', views.userDetails),
    # path('usercontestdata/<handle>', views.ContestList),
    path('contestgiven', views.CodechefUpsolveAPIView.as_view()),
]   