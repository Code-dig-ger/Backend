from django.urls import path

from . import views

urlpatterns = [
    path('search', views.SearchUser.as_view(),name="search-user"),
    path('mentor', views.MentorAPIView.as_view(), name='mentor'),
    path('testing', views.testing),
    path('rating-change-email', views.rating_change_email)

]
