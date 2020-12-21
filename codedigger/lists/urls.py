from django.urls import path
from .views import TopicwiseGetView,TopicWiseRetrieveView
urlpatterns = [
    path('topicwise/list/',TopicwiseGetView.as_view(),name='topicwise'),
    path('topicwise/list/<str:name>',TopicWiseRetrieveView.as_view(),name='topicwise-name')
]
