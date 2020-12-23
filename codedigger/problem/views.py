from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics,mixins,permissions 
from .models import Problem
from .serializers import ProbSerializer
import json

class StatusAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView,
    ):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #authentication_classes = [SessionAuthentication]
    serializer_class = ProbSerializer
    #passed_id = None 

    #running queries and stuff
    def get_queryset(self):

        qs = Problem.objects.all()
        prob = self.request.GET.get('prob_id')
        tags = self.request.GET.get('tags')
        if prob is not None:
            qs = qs.filter(prob_id__icontains = prob)
        if tags is not None:
            qs = qs.filter(tags__icontains = tags)
        return qs
       
