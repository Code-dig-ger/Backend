from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, mixins, permissions, status

# Django Models Stuff
from .models import Problem, atcoder_contest
from user.models import Profile, UserFriends
from codeforces.models import contest, user_contest_rank
from django.db.models import Q

# Serializer and Extra Utils Function

from .serializers import ProbSerializer, UpsolveContestSerializer, CCUpsolveContestSerializer, AtcoderUpsolveContestSerializer, SolveProblemsSerializer
from user.serializers import GuruSerializer, FriendsShowSerializer
from lists.models import Solved
from .utils import codeforces_status, codechef_status, atcoder_status, get_upsolve_response_dict
import json, requests
from django.http import JsonResponse
import random
from user.permissions import *
from codeforces.api import user_status
from user.exception import ValidationException


class MentorProblemAPIView(
        mixins.CreateModelMixin,
        generics.ListAPIView,
):
    permission_classes = [AuthenticatedActivated]
    serializer_class = GuruSerializer

    def get(self, request):

        #Mentors from Profile
        mentor = request.GET.get('mentor')
        #User handle from Profile
        student = Profile.objects.get(owner=self.request.user).codeforces

        #fetch student  submissions from api
        submissions_student = user_status(handle=student)
        student_solved_set = set()
        for submission in submissions_student:
            if 'contestId' in submission['problem']:
                if submission['verdict'] == 'OK':
                    student_solved_set.add(
                        str(submission["problem"]['contestId']) +
                        submission["problem"]['index'])

        if mentor != 'true':
            return Response({'status': 'OK', 'result': student_solved_set})

        guru_solved_set = set()
        guru_solved_list = []
        gurus = Profile.objects.get(
            owner=self.request.user).gurus.split(',')[1:-1]

        #print(gurus)
        for guru in gurus:
            submissions_guru = user_status(handle=guru)
            for submission in submissions_guru:

                if 'contestId' in submission['problem']:

                    if str(
                            submission["problem"]['contestId']
                    ) + submission["problem"]['index'] in guru_solved_set:
                        continue

                    elif submission['verdict'] == 'OK':
                        guru_solved_set.add(
                            str(submission["problem"]['contestId']) +
                            submission["problem"]['index'])
                        guru_solved_list.append(submission["problem"])
        #print(guru_solved_list)
        problems_data = []
        for problem in guru_solved_list:

            if str(problem["contestId"]
                   ) + problem['index'] not in student_solved_set:
                problems_data.append(
                    str(problem['contestId']) + problem['index'])

        return Response({'status': 'OK', 'result': problems_data})


class SolveProblemsAPIView(mixins.CreateModelMixin, generics.ListAPIView,
                           generics.GenericAPIView):

    permission_classes = [AuthenticatedOrReadOnly]
    serializer_class = SolveProblemsSerializer

    def get(self, request):

        tags = request.GET.get('tags')
        platforms = request.GET.get('platform')
        difficulty = request.GET.get('difficulty')
        range_l = request.GET.get('range_l')
        range_r = request.GET.get('range_r')
        searches = request.GET.get('search')
        mentors = request.GET.get('mentor')

        if request.user.is_authenticated:

            problems_list = MentorProblemAPIView.get(self, request).data

            if (problems_list['status'] != 'OK'):
                return JsonResponse(problems_list)
            else:
                problems_list = problems_list['result']

            if mentors == 'true':
                problem_qs = Problem.objects.filter(prob_id__in=problems_list)

            else:
                q = Q()
                for prob_id in problems_list:
                    q |= Q(prob_id=prob_id)
                problem_qs = Problem.objects.exclude(q)
        else:
            problem_qs = Problem.objects.all()

        if platforms is not None:
            platforms = platforms.split(',')
            problem_qs = problem_qs.filter(platform__in=platforms)

        if difficulty is not None:
            difficulty = difficulty.split(',')
            problem_qs = problem_qs.filter(difficulty__in=difficulty)

        if range_l is not None:
            problem_qs = problem_qs.filter(rating__gt=int(range_l))

        if range_r is not None:
            problem_qs = problem_qs.filter(rating__lt=int(range_r))

        if searches is not None:
            searches = searches.split(',')
            for search in searches:
                q = Q()
                q |= Q(name__icontains=search)
                q |= Q(prob_id__icontains=search)
                q |= Q(url__icontains=search)
                q |= Q(tags__icontains=search)
                q |= Q(contest_id__icontains=search)

            problem_qs = problem_qs.filter(q)

        if tags is not None:
            tags = tags.split(',')
            q = Q()

            for tag in tags:
                q |= Q(tags__icontains=tag)
            problem_qs = problem_qs.filter(q)

        problem_qs = problem_qs.order_by('?')[:20]
        return JsonResponse({
            'status':
            'OK',
            'result':
            ProbSerializer(problem_qs, many=True).data
        })


class ProblemSolvedByFriend(generics.GenericAPIView):

    permission_classes = [AuthenticatedActivated]
    serializer_class = FriendsShowSerializer

    def get(self, request, prob_id):

        problem = Problem.objects.filter(prob_id=prob_id)

        if not problem.exists():
            return Response({
                'status': 'FAILED',
                'error': 'Problem Not Found'
            },
                            status=status.HTTP_404_NOT_FOUND)

        problem = problem[0]

        userSolved = Solved.objects.filter(problem=problem).values_list(
            'user', flat=True)

        friendSolvedByRequest = UserFriends.objects.filter(
            status=True, to_user__in=userSolved, from_user=request.user)
        friendSolvedByAccept = UserFriends.objects.filter(
            status=True, to_user=request.user, from_user__in=userSolved)

        friendSolvedByRequest = FriendsShowSerializer(friendSolvedByRequest,
                                                      context={
                                                          'by_to_user': True
                                                      },
                                                      many=True).data
        friendSolvedByAccept = FriendsShowSerializer(friendSolvedByAccept,
                                                     context={
                                                         'by_to_user': False
                                                     },
                                                     many=True).data

        friendSolved = friendSolvedByRequest + friendSolvedByAccept
        return Response({'status': 'OK', 'result': friendSolved})


class UpsolveContestAPIView(
        mixins.CreateModelMixin,
        generics.ListAPIView,
):
    permission_classes = [AuthenticatedActivated]
    #authentication_classes =  [SessionAuthentication]
    serializer_class = UpsolveContestSerializer

    # passed_id = None

    #running queries  and stuff
    def get(self, request):
        handle = Profile.objects.get(owner=self.request.user).codeforces
        if handle == "" or handle == None:
            return Response(
                {
                    'status':
                    'FAILED',
                    'error':
                    'Please activate your account once by putting your name and codeforces handle..'
                },
                status=status.HTTP_400_BAD_REQUEST)

        virtual = request.GET.get('virtual')
        page = request.GET.get('page')
        path = request.build_absolute_uri('/problems/upsolve/codeforces')
        platform_name = path.rsplit('/', 1)[-1]

        if virtual != None:
            path = path + '?virtual=' + virtual + ';'
        else:
            path = path + '?'

        if page == None:
            page = 1
        elif page.isdigit():
            page = int(page)
        else:
            return Response(
                {
                    'status': 'FAILED',
                    'error': 'Page must be an integer.'
                },
                status=status.HTTP_400_BAD_REQUEST)

        RContest, VContest, SolvedInContest, Upsolved, Wrong = codeforces_status(
            handle)
        data = {
            'wrong': Wrong,
            'solved': SolvedInContest,
            'upsolved': Upsolved,
        }

        if virtual == 'true':
            RContest = RContest.union(VContest)

        c = contest.objects.filter(
            contestId__in=RContest).order_by('-startTime')

        total = c.count()
        NumPage = (total - 1) // 10 + 1  # Number of page

        if total == 0:
            return Response({'status': 'OK', 'result': []})
        if page > NumPage:
            return Response({
                'status': 'FAILED',
                'error': 'Page Out of Bound'
            },
                            status=status.HTTP_400_BAD_REQUEST)
        if page == NumPage:
            Next = None
        else:
            Next = path + 'page=' + str(page + 1)

        if page == 1:
            Prev = None
        else:
            Prev = path + 'page=' + str(page - 1)

        c = c[10 * (page - 1):10 * page]
        user_contest_details =UpsolveContestSerializer(c, many=True, context=data).data
        get_upsolve_response_dict(platform_name, user_contest_details, path, page, Prev, Next, NumPage, request, total)


class CCUpsolveContestAPIView(
        mixins.CreateModelMixin,
        generics.ListAPIView,
):
    permission_classes = [AuthenticatedActivated]
    #authentication_classes = [SessionAuthentication]
    serializer_class = CCUpsolveContestSerializer

    #passed_id = None

    def get(self, request):

        handle = Profile.objects.get(owner=self.request.user).codechef

        if handle == "" or handle == None:
            return Response(
                {
                    'status':
                    'FAILED',
                    'error':
                    'You haven\'t Entered your Codechef Username in your Profile.. Update Now!'
                },
                status=status.HTTP_400_BAD_REQUEST)

        page = request.GET.get('page')
        path = request.build_absolute_uri('/problems/upsolve/codechef')
        platform_name = path.rsplit('/', 1)[-1]

        if page == None:
            page = 1
        elif page.isdigit():
            page = int(page)
        else:
            return Response(
                {
                    'status': 'FAILED',
                    'error': 'Page must be an integer.'
                },
                status=status.HTTP_400_BAD_REQUEST)

        Upsolved, SolvedInContest, Contest, ContestName = codechef_status(
            handle)

        data = {'solved': SolvedInContest, 'upsolved': Upsolved}

        user_contest_details = []

        for contest in Contest:
            qs = Problem.objects.filter(
                Q(contest_id=contest) | Q(index=contest))

            if qs.count() > 0:
                user_contest_details.append({
                    'contestId':
                    contest,
                    'name':
                    ContestName[contest],
                    'problems':
                    CCUpsolveContestSerializer(qs, many=True,
                                               context=data).data
                })

        total = len(user_contest_details)
        NumPage = (total - 1) // 10 + 1  # Number of page

        if total == 0:
            return Response({'status': 'OK', 'result': []})
        if page > NumPage:
            return Response({
                'status': 'FAILED',
                'error': 'Page Out of Bound'
            },
                            status=status.HTTP_400_BAD_REQUEST)
        if page == NumPage:
            Next = None
        else:
            Next = path + 'page=' + str(page + 1)

        if page == 1:
            Prev = None
        else:
            Prev = path + 'page=' + str(page - 1)

        user_contest_details = user_contest_details[10 * (page - 1):10 * page]
        get_upsolve_response_dict(platform_name, user_contest_details, path, page, Prev, Next, NumPage, request, total)

class ATUpsolveContestAPIView(
        mixins.CreateModelMixin,
        generics.ListAPIView,
):
    permission_classes = [AuthenticatedActivated]
    #authentication_classes  = [SessionAuthentication]
    serializer_class = AtcoderUpsolveContestSerializer

    #passed_id  = None

    def get(self, request):

        handle = Profile.objects.get(owner=self.request.user).atcoder

        if handle == "" or handle == None:
            return Response(
                {
                    'status':
                    'FAILED',
                    'error':
                    'You haven\'t Entered your Atcoder Handle in your Profile.. Update Now!'
                },
                status=status.HTTP_400_BAD_REQUEST)

        practice = request.GET.get('practice')
        page = request.GET.get('page')
        path = request.build_absolute_uri('/problems/upsolve/atcoder')
        platform_name = path.rsplit('/', 1)[-1]

        if practice != None:
            path = path + '?practice=' + practice + ';'
        else:
            path = path + '?'

        if page == None:
            page = 1
        elif page.isdigit():
            page = int(page)
        else:
            return Response(
                {
                    'status': 'FAILED',
                    'error': 'Page must be an integer.'
                },
                status=status.HTTP_400_BAD_REQUEST)

        contests_details, all_contest, solved, wrong = atcoder_status(handle)

        if practice == 'true':
            contests_details = contests_details.union(all_contest)
        data = {'solved': solved, 'wrong': wrong}
        qs = atcoder_contest.objects.filter(
            contestId__in=contests_details).order_by('-startTime')

        total = qs.count()
        NumPage = (total - 1) // 10 + 1  # Number of page

        if total == 0:
            return Response({'status': 'OK', 'result': []})
        if page > NumPage:
            return Response({
                'status': 'FAILED',
                'error': 'Page Out of Bound'
            },
                            status=status.HTTP_400_BAD_REQUEST)
        if page == NumPage:
            Next = None
        else:
            Next = path + 'page=' + str(page + 1)

        if page == 1:
            Prev = None
        else:
            Prev = path + 'page=' + str(page - 1)

        qs = qs[10 * (page - 1):10 * page]
        user_contest_details = AtcoderUpsolveContestSerializer(qs, many=True, context=data).data
        get_upsolve_response_dict(platform_name, user_contest_details, path, page, Prev, Next, NumPage, request, total)
