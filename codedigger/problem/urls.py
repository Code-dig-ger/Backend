from django.urls import path

from .views import *

urlpatterns = [
    path('', SolveProblemsAPIView.as_view(), name="problems"),
    path('solved-by-friend/<str:prob_id>',
         ProblemSolvedByFriend.as_view(),
         name="solved-by-friend"),
    path('upsolve/codeforces',
         UpsolveContestAPIView.as_view(),
         name='cf-upsolve'),
    path('upsolve/codechef',
         CCUpsolveContestAPIView.as_view(),
         name='cc-upsolve'),
    path('upsolve/atcoder',
         ATUpsolveContestAPIView.as_view(),
         name='at-upsolve'),
]
