from django.urls import path

from . import views

urlpatterns = [
    path('' , views.ContestAPIView.as_view() , name = 'mentor.contest'),

    # Short Code Contest Url
    # path('shortCode',views.ShortCodeContestAPIView.as_view(), name='shortCodeContest'),
    # path('shortCode/<str:contestId>/standing',views.ShortCodeContestStandingAPIView.as_view(), name='Standing.shortCodeContest'),
    # path('testing' , views.testing)
]
