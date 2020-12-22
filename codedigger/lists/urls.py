from django.urls import path
from .views import TopicwiseGetListView,TopicWiseRetrieveView,TopicwiseGetLadderView,TopicWiseLadderRetrieveView
urlpatterns = [
    path('topicwise/list/',TopicwiseGetListView.as_view(),name='topicwise-list'),
    path('topicwise/list/<str:name>',TopicWiseRetrieveView.as_view(),name='topicwise-list-name'),
    path('topicwise/ladder/',TopicwiseGetLadderView.as_view(),name='topicwise-ladder'),
    path('topicwise/ladder/<str:name>',TopicWiseLadderRetrieveView.as_view(),name='topicwise-list-name'),
]
