from django.urls import path

from . import views

urlpatterns = [
    path('', views.StatusAPIView.as_view()),
    path('upsolve/codeforces' , views.UpsolveContestAPIView.as_view()),
    path('upsolve/codechef' , views.CCUpsolveContestAPIView.as_view()),
    path('upsolve/atcoder' , views.ATUpsolveContestAPIView.as_view()) ,
]
