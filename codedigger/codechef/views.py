from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import generics, serializers

from user.exception import ValidationException
from .models import CodechefContest
from .serializers import CodechefUpsolveSerializer
from .scraper_utils import contestgivenScrapper, problems_solved

from codechef.cron import *
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

        return Response({'status': 'OK', 'result' : result})

def testing(request):
    update_AllContests()
    return HttpResponse("Successfully Scrapped!")

