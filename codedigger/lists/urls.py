from django.urls import path
from .views import (
    TopicwiseGetListView,
    TopicWiseRetrieveView,
    TopicwiseGetLadderView,
    TopicWiseLadderRetrieveView,
    LevelwiseGetListView,
    LevelwiseRetrieveView,
    LevelwiseGetLadderView,
    LevelwiseLadderRetrieveView,
    updateLadderview,
    updateListView,
    UserlistCreateView,
    UserlistGetView,
    UserlistAddProblemView,
    EditUserlistView,
    AddProblemsAdminView
)



urlpatterns = [
    path('topicwise/list/',TopicwiseGetListView.as_view(),name='topicwise-list'),
    path('topicwise/list/<str:slug>',TopicWiseRetrieveView.as_view(),name='topicwise-list-name'),
    path('topicwise/ladder/',TopicwiseGetLadderView.as_view(),name='topicwise-ladder'),
    path('topicwise/ladder/<str:slug>',TopicWiseLadderRetrieveView.as_view(),name='topicwise-list-name'),
    path('levelwise/list/',LevelwiseGetListView.as_view(),name='levelwise-list'),
    path('levelwise/list/<str:slug>',LevelwiseRetrieveView.as_view(),name='levelwise-list-name'),
    path('levelwise/ladder/',LevelwiseGetLadderView.as_view(),name='levelwise-ladder'),
    path('levelwise/ladder/<str:slug>',LevelwiseLadderRetrieveView.as_view(),name='levelwise-list-name'),
    path('ladder-update',updateLadderview.as_view(),name='ladder-update'),
    path('list-update',updateListView.as_view(),name='list-update'),
    path('add-problems-admin/',AddProblemsAdminView.as_view(),name='add-problems-admin'),
    path('userlist/',UserlistGetView.as_view(),name='userlist-get'),
    path('userlist/new',UserlistCreateView.as_view(),name='userlist-create'),
    path('userlist/add',UserlistAddProblemView.as_view(),name='userlist-add'),
    path('userlist/edit/<str:slug>',EditUserlistView.as_view(),name='userlist-edit')
]
