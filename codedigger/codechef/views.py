from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import generics, serializers

from utils.exception import ValidationException
from .models import CodechefContest
from .serializers import CodechefUpsolveSerializer
from .scraper_utils import contestgivenScrapper, problems_solved
from user.models import Profile
from problem.utils import getqs, get_total_page, get_upsolve_response_dict
from codechef.cron import *
# Create your views here.


class CodechefUpsolveAPIView(generics.GenericAPIView):

    serializer_class = CodechefUpsolveSerializer

    def get(self, request):

        page = int(request.GET.get('page', 1))
        per_page = request.GET.get('per_page', 10)
        path = request.build_absolute_uri('/codechef/upsolve?')

        try:
            handle = Profile.objects.get(owner=self.request.user).codechef
        except:
            handle = request.GET.get('handle')
            path = f"{path}handle={handle}&"

        if handle == None:
            raise ValidationException(
                'Any of handle or Bearer Token is required.')

        upsolved, solved = problems_solved(handle)

        data = {'solved': solved, 'upsolved': upsolved}

        contests = contestgivenScrapper(handle)

        conts = CodechefContest.objects.filter(contestId__in=contests)

        total_contest = conts.count()
        if total_contest == 0:
            return Response({'status': 'OK', 'result': []})

        total_page = get_total_page(total_contest, per_page)

        if page != None and page > total_page:
            raise ValidationException('Page Out of Bound')

        qs = getqs(conts, per_page, page)
        result = CodechefUpsolveSerializer(qs, many=True, context=data).data
        res = get_upsolve_response_dict(result, path, page, total_contest,
                                        per_page)
        return Response(res)


def testing(request):
    update_AllContests()
    return HttpResponse("Successfully Scrapped!")
