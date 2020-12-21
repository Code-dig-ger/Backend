from rest_framework import generics,status,permissions,views
from .models import ListInfo,Solved,List
from problem.models import Problem
from user.models import User
from .serializers import TopicwiseGetSerializer,TopicwiseRetrieveSerializer

class TopicwiseGetView(generics.ListAPIView):
    serializer_class=TopicwiseGetSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = List.objects.filter(isTopicWise=True,isList=True)


class TopicWiseRetrieveView(generics.RetrieveAPIView):
    serializer_class = TopicwiseRetrieveSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = List.objects.all()
    lookup_field = "name"

    def get_serializer_context(self,**kwargs):
        data = super().get_serializer_context(**kwargs)
        data['user'] = self.request.user.username
        return data




