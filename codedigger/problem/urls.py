from django.urls import path

from . import views

urlpatterns = [
    path('', views.StatusAPIView.as_view()),
    path('upsolve/codeforces' , views.UpsolveContestAPIView.as_view()),
    path('upsolve/codechef' , views.CCUpsolveContestAPIView.as_view()),
<<<<<<< HEAD
    path('solve' , views.SolveProblemsAPIView.as_view()),
    
=======
    path('upsolve/atcoder' , views.ATUpsolveContestAPIView.as_view()) ,
>>>>>>> 1758ebb02bbb5c61120a7cd376e073f4cb57b504
]
