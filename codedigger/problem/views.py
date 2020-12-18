from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics,mixins,permissions 
from .models import Problem
from .serializers import ProbSerializer
import json

from .cron import update_spoj , update_atcoder , update_uva , update_codechef
from codeforces.cron import update_codeforces


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

def testing_spoj(request):
    update_spoj()
    return HttpResponse("OKAY")

def testing_uva(request):
    update_uva()
    return HttpResponse("OKAY")

def testing_atcoder(request):
    update_atcoder()
    return HttpResponse("OKAY")

def testing_codeforces(request):
    update_codeforces()
    return HttpResponse("OKAY")

def testing_codechef(request):
    update_codechef()
    return HttpResponse("OKAY")

       
