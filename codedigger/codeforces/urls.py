from django.urls import path

from . import views

urlpatterns = [
    path('mentor_contest' , views.MentorContestAPIView.as_view() , name = 'mentor.contest'),
    path('mentor_problem' , views.MentorProblemAPIView.as_view() , name = 'mentor.problem'),
    path('mentor' , views.MentorAPIView.as_view() , name = 'mentor'),
]