from django.urls import path

from . import views

urlpatterns = [
    path('', views.BlogAPIView.as_view(), name='blog.index'),
    path('<str:slug>', views.ABlogAPIView.as_view(), name='blog.information'),
]
