from rest_framework import generics,status,permissions,views
from .models import ListInfo,Solved,List
from problem.models import Problem
from user.models import User
from .serializers import (
    GetLadderSerializer,
    GetSerializer,
    LadderRetrieveSerializer,
    RetrieveSerializer
)
from django.db.models import Q
from .permissions import IsOwner

class TopicwiseGetListView(generics.ListAPIView):
    serializer_class=GetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list = '1') | Q(type_list = '3')) & Q(isTopicWise = True))


class TopicWiseRetrieveView(generics.RetrieveAPIView):
    serializer_class = RetrieveSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list = '1') | Q(type_list = '3')) & Q(isTopicWise = True))
    lookup_field = "slug"

    def get_serializer_context(self,**kwargs):
        data = super().get_serializer_context(**kwargs)
        data['user'] = self.request.user.username
        data['page'] = self.request.GET.get('page',1)
        return data


class TopicwiseGetLadderView(generics.ListAPIView):
    serializer_class=GetLadderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list = '2') | Q(type_list = '3')) & Q(isTopicWise = True))


class TopicWiseLadderRetrieveView(generics.RetrieveAPIView):
    serializer_class = LadderRetrieveSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list = '2') | Q(type_list = '3')) & Q(isTopicWise = True))
    lookup_field = "slug"

    def get_serializer_context(self,**kwargs):
        data = super().get_serializer_context(**kwargs)
        data['user'] = self.request.user.username
        data['page'] = self.request.GET.get('page',1)
        data['logged_in'] = self.request.user.is_authenticated
        return data


class LevelwiseGetListView(generics.ListAPIView):
    serializer_class=GetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list = '1') | Q(type_list = '3')) & Q(isTopicWise = False))


class LevelwiseRetrieveView(generics.RetrieveAPIView):
    serializer_class = RetrieveSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list = '1') | Q(type_list = '3')) & Q(isTopicWise = False))
    lookup_field = "slug"

    def get_serializer_context(self,**kwargs):
        data = super().get_serializer_context(**kwargs)
        data['user'] = self.request.user.username
        data['page'] = self.request.GET.get('page',None)
        return data


class LevelwiseGetLadderView(generics.ListAPIView):
    serializer_class=GetLadderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list = '2') | Q(type_list = '3')) & Q(isTopicWise = False))


class LevelwiseLadderRetrieveView(generics.RetrieveAPIView):
    serializer_class = LadderRetrieveSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list = '2') | Q(type_list = '3')) & Q(isTopicWise = False))
    lookup_field = "slug"

    def get_serializer_context(self,**kwargs):
        data = super().get_serializer_context(**kwargs)
        data['user'] = self.request.user.username
        data['page'] = self.request.GET.get('page',None)
        data['logged_in'] = self.request.user.is_authenticated
        return data
