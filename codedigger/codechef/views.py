from django.shortcuts import render
from django.http import HttpResponse

from codechef.cron import *
# Create your views here.

def testing(request):
    update_AllContests()
    return HttpResponse("Successfully Scrapped!")

# def ContestList():

# def ProblemList()

# def ProblemsInContest()
