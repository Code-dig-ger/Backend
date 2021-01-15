from django.urls import path

from . import views

urlpatterns = [
    path('mentor_contest/' , views.MentorContestAPIView.as_view() , name = 'mentor.contest') ,
]