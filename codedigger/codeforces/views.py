from re import A
import requests
from django.http import JsonResponse
from django.template.loader import render_to_string

from rest_framework.response import Response

from rest_framework import generics, mixins

from user.permissions import AuthenticatedActivated, AuthenticatedOrReadOnly
from user.exception import ValidationException

from user.serializers import GuruSerializer
from user.models import Profile

from lists.utils import getqs
from problem.utils import (get_page_number, get_total_page,
                           get_upsolve_response_dict)

from .api import user_info
from .api_utils import upsolve_status
from .models import contest, user
from .serializers import CodeforcesUpsolveSerializer, MiniUserSerializer


def data(URL):
    return requests.get(URL).json()


class MentorAPIView(
        mixins.CreateModelMixin,
        generics.ListAPIView,
):
    permission_classes = [AuthenticatedActivated]
    serializer_class = GuruSerializer

    def get(self, request):
        return JsonResponse({
            'status':
            'OK',
            'result':
            Profile.objects.get(owner=self.request.user).gurus.split(',')[1:-1]
        })

    def put(self, request):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.add(
                validated_data=request.data,
                instance=Profile.objects.get(owner=self.request.user))

        return Response({'status': 'OK', 'result': 'Added Successfully'})

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.delete(
            instance=Profile.objects.get(owner=self.request.user),
            data=request.data)

        return Response({'status': 'OK', 'result': 'Deleted Successfully'})


class CodeforcesUpsolveAPIView(generics.GenericAPIView):
    permission_classes = [AuthenticatedOrReadOnly]
    serializer_class = CodeforcesUpsolveSerializer

    def get_handle(self):
        handle = Profile.objects.get(owner=self.request.user).codeforces
        if handle == "" or handle == None:
            raise ValidationException(
                'Please activate your account once by putting your name and codeforces handle..'
            )
        return handle

    def get(self, request):
        is_auth = self.request.user.is_authenticated
        if not is_auth:
            handle = request.GET.get('handle', None)
            if handle == None:
                raise ValidationException(
                    'Any of handle or Bearer Token is required.')
            user_info([handle])
        else:
            handle = self.get_handle()

        virtual = request.GET.get('virtual')
        page = request.GET.get('page', None)
        per_page = request.GET.get('per_page', 10)
        path = request.build_absolute_uri('/codeforces/upsolve?')

        if not is_auth:
            path = '{}handle={};'.format(path, handle)

        if virtual != None:
            path = '{}virtual={};'.format(path, virtual)

        page = get_page_number(page)

        RContest, VContest, PContest, \
            SolvedInContest, Upsolved, Wrong = upsolve_status(handle)

        data = {
            'wrong': Wrong,
            'solved': SolvedInContest,
            'upsolved': Upsolved,
        }

        if virtual == 'true':
            RContest = RContest.union(VContest)

        c = contest.objects.filter(contestId__in=RContest)\
                            .order_by('-startTime')

        total_contest = c.count()
        if total_contest == 0:
            return Response({'status': 'OK', 'result': []})

        total_page = get_total_page(total_contest, per_page)
        if page > total_page:
            raise ValidationException('Page Out of Bound')

        user_contest_details = CodeforcesUpsolveSerializer(getqs(
            c, per_page, page),
                                                           many=True,
                                                           context=data).data
        res = get_upsolve_response_dict(user_contest_details, path, page,
                                        total_contest, per_page)
        return Response(res)


# from .cron import codeforces_update_problems
from django.template.loader import render_to_string
from django.http import HttpResponse
from .test_fixtures.rating_change_fixture import contest_rank, rating_change
from .utils import *
from codeforces.api import contest_submissions

def testing(request):
    submissions =contest_submissions(contestId=1619,count=10)
    print(submissions)
    return JsonResponse({'status': 'OK'})


class SearchUser(
        mixins.CreateModelMixin,
        generics.ListAPIView,
):
    permission_classes = [AuthenticatedOrReadOnly]
    serializer_class = MiniUserSerializer

    def get(self, request):
        user_name = request.GET.get('q').lower()
        relevant_users = user.objects.filter(handle__istartswith=user_name)
        final_users = MiniUserSerializer(relevant_users[:5], many=True).data
        return Response({'status': 'OK', 'result': final_users})


def rating_change_email(request):

    rating_change.update({
        'oldRank':
        rating_to_rank(rating_change['oldRating']),
        'newRank':
        rating_to_rank(rating_change['newRating']),
        'oldcolor':
        rating_to_color(rating_change['oldRating']),
        'newcolor':
        rating_to_color(rating_change['newRating']),
        'isoldlegendary':
        islegendary(rating_change['oldRating']),
        'isnewlegendary':
        islegendary(rating_change['newRating'])
    })

    context = {'rating_change': rating_change, 'cdata': contest_rank}

    print(context)
    return HttpResponse(
        render_to_string('codeforces/rating_reminder.html', context))
