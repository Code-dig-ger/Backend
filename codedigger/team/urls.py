from django.urls import path
from .views import RegisterTeam,TeamGetView
urlpatterns = [
    path('register/', RegisterTeam.as_view(), name="register"),
    path('userteams/<int:user_id>',TeamGetView.as_view(),name='get_teams')
]