from django.shortcuts import render
from .scraper import go_scraper
from django.http import HttpResponse

# Create your views here.


def testing(request):
    go_scraper()
    return HttpResponse("Successfully Scrapped!")


# def ContestList():

# def ProblemList()

# def ProblemsInContest()
