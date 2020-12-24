from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics,mixins,permissions 

from .models import user,country,organization,contest,user_contest_rank
from problem.models import Problem
from user.models import Profile

from .serializers import UserSerializer,CountrySerializer,OrganizationSerializer,ContestSerializer
from .serializers import UpsolveContestSerializer
from problem.serializers import ProbSerializer
import json
from .utils import codeforces_status

from django.http import HttpResponse


class UsersAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView,
    ):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #authentication_classes = [SessionAuthentication]
    serializer_class = UserSerializer
    #passed_id = None 

    #running queries and stuff
    def get_queryset(self):

        qs = user.objects.all()
        handle = self.request.GET.get('handle')
        if handle is not None:
            qs = qs.filter(handle = handle)
        return qs

class ProblemsAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView,
    ):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #authentication_classes = [SessionAuthentication]
    serializer_class = ProbSerializer
    #passed_id = None 

    #running queries and stuff
    def get_queryset(self):

        qs = Problem.objects.all().filter(platform = 'F')
        tags = self.request.GET.get('tags')
        if tags is not None:
            qs = qs.filter(tags_icontains = tags)
        return qs

class CountryAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView,
    ):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #authentication_classes = [SessionAuthentication]
    serializer_class = CountrySerializer
    #passed_id = None 

    #running queries and stuff
    def get_queryset(self):

        qs = country.objects.all()
        name = self.request.GET.get('name')
        if name is not None:
            qs = qs.filter(name = name)
        return qs

class OrganizationAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView,
    ):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #authentication_classes = [SessionAuthentication]
    serializer_class = OrganizationSerializer
    #passed_id = None 

    #running queries and stuff
    def get_queryset(self):

        qs = organization.objects.all()
        name = self.request.GET.get('name')
        if name is not None:
            qs = qs.filter(name = name)
        return qs


class ContestAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView,
    ):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #authentication_classes = [SessionAuthentication]
    serializer_class = ContestSerializer
    #passed_id = None 

    #running queries and stuff
    def get_queryset(self):

        qs = contest.objects.all()
        contestId = self.request.GET.get('contestId')
        if contestId is not None:
            qs = qs.filter(contestId = contestId)
        return qs


SolvedInContest = None
Upsolved = None 
Wrong = None

class UpsolveContestAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView,
    ):
    permission_classes = [permissions.IsAuthenticated]
    #authentication_classes = [SessionAuthentication]
    serializer_class = UpsolveContestSerializer
    #passed_id = None 

    #running queries and stuff
    def get_queryset(self):
        global SolvedInContest 
        global Upsolved 
        global Wrong
        handle = Profile.objects.get(owner =self.request.user).codeforces
        RContest , VContest , SolvedInContest , Upsolved , Wrong = codeforces_status(handle)
        c = contest.objects.filter(contestId__in = list(RContest))
        return c

    def get_serializer_context(self,**kwargs):
        data = super().get_serializer_context(**kwargs)
        data['wrong'] = Wrong
        data['solved'] = SolvedInContest
        data['upsolved'] = Upsolved
        return data







