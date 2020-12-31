from rest_framework import generics,status,permissions,views,response
from .models import ListInfo,Solved,List
from problem.models import Problem
from user.models import User,Profile
from .serializers import (
    GetLadderSerializer,
    GetSerializer,
    LadderRetrieveSerializer,
    RetrieveSerializer
)
from django.db.models import Q
from .permissions import IsOwner
from .solved_update import codeforces,uva,atcoder,codechef,spoj
from .cron import updater

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
        data['page'] = self.request.GET.get('page',None)
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
        data['page'] = self.request.GET.get('page',None)
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


class updateLadderview(views.APIView):
    def get(self,request,*args, **kwargs):
        prob_id = self.request.GET.get('prob_id')
        if prob_id is None:
            codeforces(self.request.user.username)
            uva(self.request.user.username)
            atcoder(self.request.user.username)
        else:
            if Problem.objects.filter(prob_id=prob_id,platform='C').exists():
                codechef(self.request.user.username,prob_id)
            if Problem.objects.filter(prob_id=prob_id,platform='S').exists():
                spoj(self.request.user.username,prob_id)
        return response.Response(data={'status' : 'ok'})
