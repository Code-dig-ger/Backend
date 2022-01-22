from django.urls import path
from . import views

urlpatterns = [
    path('upsolve',
         views.CodechefUpsolveAPIView.as_view(),
         name="codechef-upsolve"),
    path('recentsub/<str:username>',
         views.CodechefRecentSubmissionAPIView.as_view()),
    path('problemsub/<str:username>/<str:problem>',
         views.CodechefUserSubmissionAPIView.as_view()),
    path('contestproblems/<str:contest>',
         views.CodechefContestProblemsAPIView.as_view()),
    path('contests/<str:time>/<str:typec>',
         views.CodechefContestsAPIView.as_view()),
    path('testing', views.testing)
]
