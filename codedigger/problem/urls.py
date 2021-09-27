from django.urls import path

from . import views

urlpatterns = [
    path(
        '',
        views.SolveProblemsAPIView.as_view()),
    path(
        'solved-by-friend/<str:prob_id>',
        views.ProblemSolvedByFriend.as_view()),
    path(
        'upsolve/codeforces',
        views.UpsolveContestAPIView.as_view()),
    path(
        'upsolve/codechef',
        views.CCUpsolveContestAPIView.as_view()),
    path(
        'upsolve/atcoder',
        views.ATUpsolveContestAPIView.as_view()),
]
