from django.urls import path

from .views import StatusAPIView
from . import views

urlpatterns = [
    path('', StatusAPIView.as_view()),
    path('testing/spoj' ,views.testing_spoj),
    path('testing/uva' ,views.testing_uva),
    path('testing/atcoder' ,views.testing_atcoder),
    path('testing/codeforces' ,views.testing_codeforces),
    path('testing/codechef' ,views.testing_codechef),
]
