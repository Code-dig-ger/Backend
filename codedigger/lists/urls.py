from django.urls import path
from .views import (
    TopicwiseGetListView,
    TopicWiseRetrieveView,
    TopicwiseGetLadderView,
    TopicWiseLadderRetrieveView,
    LevelwiseGetListView,
    LevelwiseRetrieveView,
    LevelwiseGetLadderView,
    LevelwiseLadderRetrieveView
)



urlpatterns = [
    path('topicwise/list/',TopicwiseGetListView.as_view(),name='topicwise-list'),
    path('topicwise/list/<str:name>',TopicWiseRetrieveView.as_view(),name='topicwise-list-name'),
    path('topicwise/ladder/',TopicwiseGetLadderView.as_view(),name='topicwise-ladder'),
    path('topicwise/ladder/<str:name>',TopicWiseLadderRetrieveView.as_view(),name='topicwise-list-name'),
    path('levelwise/list/',LevelwiseGetListView.as_view(),name='levelwise-list'),
    path('levelwise/list/<str:name>',LevelwiseRetrieveView.as_view(),name='levelwise-list-name'),
    path('levelwise/ladder/',LevelwiseGetLadderView.as_view(),name='levelwise-ladder'),
    path('levelwise/ladder/<str:name>',LevelwiseLadderRetrieveView.as_view(),name='levelwise-list-name'),

]
