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




def testing(request):
    return JsonResponse({'status': 'OK'})


class SearchUser(
        mixins.CreateModelMixin,
        generics.ListAPIView,
):

    def get(self, request):
        user_name = request.GET.get('search').lower()
        all_users = user.objects.all()
        relevant_users = []
        for current_user in all_users:
            handle = current_user.handle.lower()
            name = ""
            if current_user.name != None:
                name = current_user.name.lower()
            i = 0
            score1,score2 = 0,0
            while i<min(len(handle),len(user_name)):
                if handle[i] == user_name[i]:
                    score1 += 1
                else:
                    break
                i+=1
            i = 0
            while i<min(len(name),len(user_name)):
                if name[i] == user_name[i]:
                    score2 += 1
                else:
                    break
                i+=1
            relevant_users.append([max(score1,score2),current_user])
        
        relevant_users.sort(key = lambda x: x[0],reverse = True)
        final_users = []
        for i in range(5):
            dict1 = {}
            dict1["name"] = relevant_users[i][1].name
            dict1["handle"] = relevant_users[i][1].handle
            dict1["profile"] = relevant_users[i][1].photoUrl
            final_users.append(dict1)

        return JsonResponse({
            'status':
            'OK',
            'result':
                final_users
        })
