from django.urls import path

from . import views

urlpatterns = [
    path('', views.ContestAPIView.as_view(), name='contest.filter'),
    # Below Urls are specifically for Codedigger Extension
    path('codeforces/<str:handle>',
         views.CodeforcesContestAPIView.as_view(),
         name='codeforces.contest'),
    path('codeforces/<str:handle>/<int:contestId>',
         views.CodeforcesContestGetAPIView.as_view(),
         name='codeforces.contest.get'),
     path('codeforces/<str:handle>/<int:contestId>/submissions',
         views.CodeforcesContestSubmissionsGetAPIView.as_view(),
         name='codeforces.contest.submissions'),
    path('codeforces/<str:handle>/<str:probId>',
         views.CodeforcesProblemCheckAPIView.as_view(),
         name='codeforces.problem.check')

    # Short Code Contest Url
    #path('shortCode',views.ShortCodeContestAPIView.as_view(), name='shortCodeContest'),
    # path('shortCode/<str:contestId>/standing',views.ShortCodeContestStandingAPIView.as_view(), name='Standing.shortCodeContest'),
    # path('testing' , views.testing)
]
