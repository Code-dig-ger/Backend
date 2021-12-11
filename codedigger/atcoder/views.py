from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, mixins, permissions, status

# Django Models Stuff
from problem.models import Problem, atcoder_contest
from user.models import Profile, UserFriends
from codeforces.models import contest, user_contest_rank
from django.db.models import Q

# Serializer and Extra Utils Function

from problem.serializers import ProbSerializer, UpsolveContestSerializer, CCUpsolveContestSerializer, AtcoderUpsolveContestSerializer, SolveProblemsSerializer
from user.serializers import GuruSerializer, FriendsShowSerializer
from lists.models import Solved
from problem.utils import codeforces_status, codechef_status, atcoder_status, get_page_number, get_upsolve_response_dict
import json, requests
from django.http import JsonResponse
import random
from user.permissions import *
from codeforces.api import user_status
from user.exception import ValidationException
from lists.utils import get_total_page, getqs

# Create your views here.

class ATUpsolveContestAPIView(
        mixins.CreateModelMixin,
        generics.ListAPIView,
):
    permission_classes = [AuthenticatedOrReadOnly]

    serializer_class = AtcoderUpsolveContestSerializer

    def get(self, request):
        is_auth = self.request.user.is_authenticated
        handle = ""
        if not is_auth:
            handle = request.GET.get('handle', None)
            if handle == None:
                raise ValidationException(
                    'Any of handle or Bearer Token is required.')
        else:
            handle = Profile.objects.get(owner=self.request.user).atcoder

        if handle == "" or handle == None:
            raise ValidationException(
                'You haven\'t Entered your Atcoder Handle in your Profile.. Update Now!'
            )

        practice = request.GET.get('practice')
        page = request.GET.get('page', None)
        per_page = request.GET.get('per_page', 10)
        path = request.build_absolute_uri('/problems/upsolve/atcoder?')

        if practice != None:
            path = '{}practice={};'.format(path, practice)

        page = get_page_number(page)

        contests_details, all_contest, solved, wrong = atcoder_status(handle)

        if practice == 'true':
            contests_details = contests_details.union(all_contest)
        data = {'solved': solved, 'wrong': wrong}
        qs = atcoder_contest.objects.filter(
            contestId__in=contests_details).order_by('-startTime')

        total_contest = qs.count()
        if total_contest == 0:
            return Response({'status': 'OK', 'result': []})
        total_page = get_total_page(total_contest, per_page)
        if page > total_page:
            raise ValidationException('Page Out of Bound')

        qs = getqs(qs, per_page, page)
        user_contest_details = AtcoderUpsolveContestSerializer(
            qs, many=True, context=data).data
        res = get_upsolve_response_dict(user_contest_details, path, page,
                                        total_contest, per_page)
        return Response(res)
