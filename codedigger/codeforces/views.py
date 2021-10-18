from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, mixins, permissions
from django.core import serializers
from .models import user, country, organization, contest
from .serializers import MiniUserSerializer, UserSerializer, CountrySerializer, OrganizationSerializer, ContestSerializer
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




def testing(request):
    return JsonResponse({'status': 'OK'})


class SearchUser(
        mixins.CreateModelMixin,
        generics.ListAPIView,
):
    permission_classes = [AuthenticatedOrReadOnly]
    serializer_class = MiniUserSerializer

    def get(self, request):
        user_name = request.GET.get('q').lower()
        relevant_users = user.objects.filter(handle__istartswith=user_name)
        final_users = MiniUserSerializer(relevant_users[:5], many = True).data
        return Response({
            'status':
            'OK',
            'result':
                final_users
        })