from django.db.models import Q
from rest_framework.response import Response
from rest_framework import generics, mixins, status

# Exceptions and Permissions
from user.exception import ValidationException
from user.permissions import *

# Models Stuff
from user.models import Profile, UserFriends
from codeforces.models import contest
from lists.models import Solved
from .models import Problem, atcoder_contest

# Serializers
from user.serializers import GuruSerializer, FriendsShowSerializer
from .serializers import (ProbSerializer, UpsolveContestSerializer,
                          CCUpsolveContestSerializer,
                          AtcoderUpsolveContestSerializer)

# Utility Functions
from codeforces.api_utils import wrong_submissions, multiple_correct_submissions
from lists.utils import get_total_page, getqs
from .utils import (codeforces_status, codechef_status, atcoder_status,
                    get_page_number, get_upsolve_response_dict)


class SolveProblemsAPIView(mixins.CreateModelMixin, generics.ListAPIView,
                           generics.GenericAPIView):

    permission_classes = [AuthenticatedOrReadOnly]
    serializer_class = ProbSerializer

    def get(self, request):

        tags = request.GET.get('tags')
        and_in_tags = request.GET.get('and_in_tags', 'false').lower()
        platforms = request.GET.get('platform')
        difficulty = request.GET.get('difficulty')
        range_l = request.GET.get('range_l')
        range_r = request.GET.get('range_r')
        searches = request.GET.get('search')
        mentor = request.GET.get('mentor', 'false').lower()
        only_wrong = request.GET.get('only_wrong', 'false').lower()
        hide_solved = request.GET.get('hide_solved', 'false').lower()
        index = request.GET.get('index')

        problem_qs = Problem.objects.all()

        if request.user.is_authenticated:

            user_profile = Profile.objects.get(owner=self.request.user)
            if user_profile.codeforces == None or user_profile.codeforces == "":
                raise ValidationException(
                    'Please Activate your account by updating your Profile.')

            if mentor == 'true':
                mentors = user_profile.gurus.split(',')[1:-1]
                if len(mentors) == 0:
                    raise ValidationException(
                        'Please add some mentors in your Profile to use this filter.'
                    )

                mentors_correct = multiple_correct_submissions(mentors)
                problem_qs = problem_qs.filter(prob_id__in=mentors_correct)

            if only_wrong == 'true':
                wrong = wrong_submissions(user_profile.codeforces)
                problem_qs = problem_qs.filter(prob_id__in=wrong)

            if hide_solved == 'true':
                solved_prob = Solved.objects.filter(user=request.user)
                problem_qs = problem_qs.exclude(
                    id__in=[o.problem.id for o in solved_prob])

        if platforms is not None:
            platforms = platforms.split(',')
            problem_qs = problem_qs.filter(platform__in=platforms)

        rating_q = Q()
        rating_q |= (Q(platform='A') & Q(difficulty__isnull=False))
        rating_q |= Q(rating__endswith='00')
        rating_q |= (Q(platform='C') & Q(difficulty__isnull=False))

        if difficulty is not None:
            difficulty = difficulty.split(',')
            problem_qs = problem_qs.filter(rating_q)\
                                   .filter(difficulty__in=difficulty)

        if range_l is not None:
            problem_qs = problem_qs.filter(rating_q)\
                                   .filter(rating__gt=int(range_l))

        if range_r is not None:
            problem_qs = problem_qs.filter(rating_q)\
                                   .filter(rating__lt=int(range_r))

        if index is not None:
            indices = index.split(',')
            q = Q()
            for index in indices:
                q |= Q(index__iexact=index)
            problem_qs = problem_qs.filter(q)

        if searches is not None:
            searches = searches.split(',')
            q = Q()
            for search in searches:
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
                if and_in_tags == 'true':
                    q &= Q(tags__icontains=tag)
                else:
                    q |= Q(tags__icontains=tag)
            problem_qs = problem_qs.filter(q)

        problem_qs = problem_qs.order_by('?')[:20]
        return Response({
            'status': 'OK',
            'result': ProbSerializer(
                    problem_qs,
                    many=True,
                    context={
                        'user': request.user if request.user.is_authenticated \
                                else None
                    }
                ).data
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
    # Deprecated
    permission_classes = [AuthenticatedActivated]
    serializer_class = UpsolveContestSerializer

    def get(self, request):
        handle = Profile.objects.get(owner=self.request.user).codeforces
        if handle == "" or handle == None:
            raise ValidationException(
                'Please activate your account once by putting your name and codeforces handle..'
            )

        virtual = request.GET.get('virtual')
        page = request.GET.get('page', None)
        per_page = request.GET.get('per_page', 10)
        path = request.build_absolute_uri('/problems/upsolve/codeforces?')

        if virtual != None:
            path = '{}virtual={};'.format(path, virtual)

        page = get_page_number(page)

        RContest, VContest, SolvedInContest, Upsolved, Wrong = \
                                        codeforces_status(handle)
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

        user_contest_details = UpsolveContestSerializer(getqs(
            c, per_page, page),
                                                        many=True,
                                                        context=data).data
        res = get_upsolve_response_dict(user_contest_details, path, page,
                                        total_contest, per_page)
        return Response(res)


class CCUpsolveContestAPIView(
        mixins.CreateModelMixin,
        generics.ListAPIView,
):
    permission_classes = [AuthenticatedActivated]
    serializer_class = CCUpsolveContestSerializer

    def get(self, request):

        handle = Profile.objects.get(owner=self.request.user).codechef

        if handle == "" or handle == None:
            raise ValidationException(
                'You haven\'t Entered your Codechef Username in your Profile.. Update Now!'
            )

        page = request.GET.get('page', None)
        per_page = request.GET.get('per_page', 10)
        path = request.build_absolute_uri('/problems/upsolve/codechef?')

        page = get_page_number(page)

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

        total_contest = len(user_contest_details)
        if total_contest == 0:
            return Response({'status': 'OK', 'result': []})
        total_page = get_total_page(total_contest, per_page)
        if page > total_page:
            raise ValidationException('Page Out of Bound')

        user_contest_details = getqs(user_contest_details, per_page, page)
        res = get_upsolve_response_dict(user_contest_details, path, page,
                                        total_contest, per_page)
        return Response(res)


class ATUpsolveContestAPIView(
        mixins.CreateModelMixin,
        generics.ListAPIView,
):
    permission_classes = [AuthenticatedActivated]
    serializer_class = AtcoderUpsolveContestSerializer

    def get(self, request):

        handle = Profile.objects.get(owner=self.request.user).atcoder

        if handle == "" or handle == None:
            raise ValidationException(
                'You haven\'t Entered your Atcoder Handle in your Profile.. Update Now!'
            )

        practice = request.GET.get('practice')
        page = request.GET.get('page', None)
        per_page = request.GET.get('per_page', 10)
        path = request.build_absolute_uri('/problems/upsolve/atcoder?')

        if practice != None:
            path = '{}practice={};'.format(path, practice)

        page = get_page_number(page)

        contests_details, all_contest, solved, wrong = atcoder_status(handle)

        if practice == 'true':
            contests_details = contests_details.union(all_contest)
        data = {'solved': solved, 'wrong': wrong}
        qs = atcoder_contest.objects.filter(
            contestId__in=contests_details).order_by('-startTime')

        total_contest = qs.count()
        if total_contest == 0:
            return Response({'status': 'OK', 'result': []})
        total_page = get_total_page(total_contest, per_page)
        if page > total_page:
            raise ValidationException('Page Out of Bound')

        qs = getqs(qs, per_page, page)
        user_contest_details = AtcoderUpsolveContestSerializer(
            qs, many=True, context=data).data
        res = get_upsolve_response_dict(user_contest_details, path, page,
                                        total_contest, per_page)
        return Response(res)
