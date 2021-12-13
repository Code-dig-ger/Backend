from django.shortcuts import render
from django.http import HttpResponse
from .scraper import userScraper

# Create your views here.

def testing(request):
    return HttpResponse("Successfully Scrapped!")

def userDetails(request, handle):
    print(handle)
    userScraper(handle)
    return HttpResponse("user saved")


# def ContestList():

# def ProblemList()

# def ProblemsInContest()
