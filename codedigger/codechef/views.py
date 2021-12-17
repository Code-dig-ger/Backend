from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import generics, serializers

from .models import CodechefContest
from .serializers import CodechefUpsolveSerializer
from .scraper_utils import contestgivenScrapper, userScraper
from problem.scraper.codechef import codeChefScraper
from problem.scraper.autocodechef import autoCodechefScrap

# Create your views here.

def testing(request):
    return HttpResponse("Successfully Scrapped!")

def userDetails(request, handle):
    print(handle)
    userScraper(handle)
    return HttpResponse("user saved")


def ContestList(request, handle):
    contestgivenScrapper(handle)
    return HttpResponse("users contest collected")

# def ProblemList()

# def ProblemsInContest()

class CodechefUpsolveAPIView(generics.GenericAPIView):
    
    serializer_class = CodechefUpsolveSerializer

    def get(self, request):
        handle = 'anubhavtyagi'
        contests = contestgivenScrapper(handle)
        resp = []
        # codeChefScraper()
        for contest in contests:
            cont, isCreated = CodechefContest.objects.get_or_create(contestId = contest)
            resp.append(CodechefUpsolveSerializer(cont).data)

        return Response({'result' : resp})
