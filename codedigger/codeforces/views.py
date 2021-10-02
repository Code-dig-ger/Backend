from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, mixins, permissions

from .models import user, country, organization, contest
from .serializers import UserSerializer, CountrySerializer, OrganizationSerializer, ContestSerializer
from user.serializers import GuruSerializer
from problem.serializers import ProbSerializer
import json, requests
from django.http import JsonResponse
from user.models import Profile
from django.db.models import Q

from django.template.loader import render_to_string
from user.permissions import *


def data(URL):
    return requests.get(URL).json()


class MentorAPIView(
        mixins.CreateModelMixin,
        generics.ListAPIView,
):
    permission_classes = [AuthenticatedActivated]
    serializer_class = GuruSerializer

    def get(self, request):
        return JsonResponse({
            'status':
            'OK',
            'result':
            Profile.objects.get(owner=self.request.user).gurus.split(',')[1:-1]
        })

    def put(self, request):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.add(
                validated_data=request.data,
                instance=Profile.objects.get(owner=self.request.user))

        return Response({'status': 'OK', 'result': 'Added Successfully'})

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.delete(
            instance=Profile.objects.get(owner=self.request.user),
            data=request.data)

        return Response({'status': 'OK', 'result': 'Deleted Successfully'})


from .cron import codeforces_update_problems
from django.template.loader import render_to_string
from django.http import HttpResponse
from .test_fixtures.rating_change_fixture import contest_rank, rating_change
from .utils import *

def testing(request):
    codeforces_update_problems()
    return JsonResponse({'status': 'OK'})


def rating_change_email(request):

    rating_change.update({
        'oldRank':
        rating_to_rank(rating_change['oldRating']),
        'newRank':
        rating_to_rank(rating_change['newRating']),
        'oldcolor':
        rating_to_color(rating_change['oldRating']),
        'newcolor':
        rating_to_color(rating_change['newRating']),
        'isoldlegendary':
        islegendary(rating_change['oldRating']),
        'isnewlegendary':
        islegendary(rating_change['newRating'])
    })

    context = {
        'rating_change': rating_change, 
        'cdata': contest_rank
    }

    print (context)
    return HttpResponse(render_to_string('codeforces/rating_reminder.html', context))