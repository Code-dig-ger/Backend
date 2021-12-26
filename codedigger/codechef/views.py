from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import generics, serializers

from user.exception import ValidationException
from .models import CodechefContest
from .serializers import CodechefUpsolveSerializer
from .scraper_utils import contestgivenScrapper, problems_solved, userScraper
from problem.scraper.codechef import codeChefScraper
from problem.scraper.autocodechef import autoCodechefScrap

# Create your views here.

class CodechefUpsolveAPIView(generics.GenericAPIView):
    
    serializer_class = CodechefUpsolveSerializer

    def get(self, request, username):
    
        handle = request.GET.get('handle', username)
        if handle == None:
            raise ValidationException('Any of handle or Bearer Token is required.')

        upsolved, solved = problems_solved(handle)
        
        data = {
            'solved' : solved,
            'upsolved' : upsolved
        }

        contests = contestgivenScrapper(handle)

        conts = CodechefContest.objects.filter(contestId__in=contests)
        result = CodechefUpsolveSerializer(conts, many=True, context=data).data

        return Response({'result' : result})
