from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import generics, serializers

from user.exception import ValidationException
from .models import CodechefContest
from .serializers import CodechefUpsolveSerializer
from .scraper_utils import contestgivenScrapper, problems_solved, RecentSubmission, UserSubmissionDetails

from codechef.cron import *
# Create your views here.


class CodechefUpsolveAPIView(generics.GenericAPIView):

    serializer_class = CodechefUpsolveSerializer

    def get(self, request, username):

        handle = request.GET.get('handle', username)
        if handle == None:
            raise ValidationException(
                'Any of handle or Bearer Token is required.')

        upsolved, solved = problems_solved(handle)

        data = {'solved': solved, 'upsolved': upsolved}

        contests = contestgivenScrapper(handle)

        conts = CodechefContest.objects.filter(contestId__in=contests)
        result = CodechefUpsolveSerializer(conts, many=True, context=data).data

        return Response({'status': 'OK', 'result': result})


class CodechefRecentSubmissionAPIView(generics.GenericAPIView):

    def get(self, request, username):

        handle = request.GET.get('handle', username)
        if handle == None:
            raise ValidationException(
                'Any of handle or Bearer Token is required.')

        result = RecentSubmission(handle)

        return Response({'status': 'OK', 'result': result})


class CodechefUserSubmissionAPIView(generics.GenericAPIView):

    def get(self, request, username, problem):

        handle = request.GET.get('handle', username)
        problemcode = request.GET.get('problemcode', problem)
        if handle == None:
            raise ValidationException(
                'Any of handle or Bearer Token is required.')
        
        if problemcode == None:
            raise ValidationException(
                'Any of valid problem code is required.')

        result = UserSubmissionDetails(problemcode, handle)

        return Response({'status': 'OK', 'result': result})


class CodechefContestProblemsAPIView(generics.GenericAPIView):

    def get(self, request, contest):

        contest_id = request.GET.get('contest_id', contest)

        if contest_id == None:
            raise ValidationException(
                'A valid Contest ID is required.')

        result = ProblemData(contest_id)

        return Response({'status': 'OK', 'result': result})

def testing(request):
    update_AllContests()
    return HttpResponse("Successfully Scrapped!")
