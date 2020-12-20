from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics,mixins,permissions 

from .models import user,country,organization,contest,user_contest_rank
from .models import organization_contest_participation, country_contest_participation
from problem.models import Problem

from .serializers import UserSerializer,CountrySerializer,OrganizationSerializer,ContestSerializer
from .serializers import contestRankSerializer
from problem.serializers import ProbSerializer
import json

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

class ContestRankAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView,
    ):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #authentication_classes = [SessionAuthentication]
    serializer_class = contestRankSerializer
    #passed_id = None 

    #running queries and stuff
    def get_queryset(self):

        qs = user_contest_rank.objects.all()
        contestId = self.request.GET.get('contestId')
        if contestId is not None:
            qs = qs.filter(contestId = contestId)
        return qs




### TESTING CODEFORCES STUFF

from .cron import codeforces_update_users , codeforces_update_problems , codeforces_update_contest


def testing_users(request):
    codeforces_update_users()
    return HttpResponse("OKAY")


def testing_problems(request):
    codeforces_update_problems()
    return HttpResponse("OKAY")


def testing_contest(request):
    codeforces_update_contest()
    return HttpResponse("OKAY")


