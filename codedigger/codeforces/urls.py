from django.urls import path

from . import views

urlpatterns = [
    path('problems', views.ProblemsAPIView.as_view(), name='problem.index'),
    path('users', views.UsersAPIView.as_view(), name='user.index'),
    path('organization', views.OrganizationAPIView.as_view(), name='organization.index'),
    path('country', views.CountryAPIView.as_view(), name='country.index'),
    path('contest', views.ContestAPIView.as_view(), name='contest.index'),

    path('mentor_contest' , views.MentorContestAPIView.as_view() , name = 'mentor.contest'),
    path('mentor_problem' , views.MentorProblemAPIView.as_view() , name = 'mentor.problem'),
    path('mentor' , views.MentorAPIView.as_view() , name = 'mentor'),


    path('testing' , views.testing)

]