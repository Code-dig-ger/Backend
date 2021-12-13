from datetime import timedelta, datetime, timezone
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import generics, mixins, status

# Exceptions and Permissions
from user.exception import ValidationException
from user.permissions import *

# Models
from user.models import Profile
from codeforces.models import contest
from .models import *

# Serializers
from codeforces.serializers import ContestSerializer
from .serializers import CodeforcesContestSerializer, MiniCodeforcesContestSerializer

# Utility Functions
from codeforces.api import user_status
from codeforces.api_utils import (codeforces_user_submissions,
                                  get_correct_submissions,
                                  get_wrong_submission)
from codeforces.codeforcesProblemSet import get_similar_problems
from codeforces.models_utils import validate_handle
from .model_utils import get_contest_problem_qs, get_user_contests


class ContestAPIView(
        mixins.CreateModelMixin,
        generics.ListAPIView,
):
    permission_classes = [AuthenticatedActivated]
    serializer_class = ContestSerializer

    def get(self, request):
        # Contest Filter
        gym = request.GET.get('gym')
        divs = request.GET.get('divs')
        mentor = request.GET.get('mentor')
        timeline = request.GET.get('timeline')

        gurus = Profile.objects.get(
            owner=self.request.user).gurus.split(',')[1:-1]
        students = [Profile.objects.get(owner=self.request.user).codeforces]
        #TODO convert to list

        #fetch student data from api
        student_contests = set()
        for student in students:
            submissions_student = user_status(handle=student)
            for submission in submissions_student:
                if (submission['verdict'] == 'OK'):
                    student_contests.add(submission["problem"]["contestId"])
        if mentor == 'true':
            guru_contests = set()
            for guru in gurus:
                submissions_guru = user_status(handle=guru)
                for submission in submissions_guru:
                    if 'contestId' not in submission['problem']:
                        continue
                    if (submission['author']['participantType'] !=
                            'PRACTICE') & (submission['verdict'] == 'OK'):
                        guru_contests.add(submission["problem"]["contestId"])
            #Select contest Ids which are not in student set
            contest_list = []
            for contest_ in guru_contests:
                if contest_ not in student_contests:
                    contest_list.append(contest_)

            contest_qs = contest.objects.filter(contestId__in=contest_list)
        else:
            q = Q()
            for contestId in student_contests:
                q |= Q(contestId=contestId)
            contest_qs = contest.objects.exclude(q)

        if gym != 'true':
            contest_qs = contest_qs.filter(Type='R')

        if divs != None:
            divs = divs.split(',')
            q = Q()
            for div in divs:
                q |= Q(name__icontains=div)
            contest_qs = contest_qs.filter(q)

        # TODO Timeline
        # if timeline != None:
        # time = current_time - timeline * month_time
        # contest_qs = contest_qs.filter(startTime__gt > time)

        contest_qs = contest_qs.order_by('?')[:20]
        context = {
            'status': 'OK',
            'result': ContestSerializer(contest_qs, many=True).data
        }

        return Response(context)


# Codeforces Contest Views Start
# These Views are specifically designed for Codedigger Extension
class CodeforcesContestAPIView(generics.GenericAPIView):
    permission_classes = [AuthenticatedOrReadOnly]
    serializer_class = MiniCodeforcesContestSerializer

    def get(self, request, handle):
        codeforcesUser = validate_handle(handle)
        contests = get_user_contests(codeforcesUser)

        return Response({
            'status':
            'OK',
            'result':
            MiniCodeforcesContestSerializer(contests, many=True).data
        })

    def post(self, request, handle):
        codeforcesUser = validate_handle(handle)
        pastContests = get_user_contests(codeforcesUser)

        if pastContests.exists() and datetime.now(tz=timezone.utc) <= \
                pastContests[0].startTime + timedelta(seconds= pastContests[0].duration):
            raise ValidationException('contest is running')

        newContest = CodeforcesContest()
        newContest.owner = codeforcesUser
        newContest.name = "Codedigger Contest #{} #{}".format(
            handle,
            pastContests.count() + 1)
        newContest.save()

        # TODO Assign Problems to this Contest
        # https://github.com/cheran-senthil/TLE/blob/master/tle/cogs/codeforces.py#L178

        return Response({'status': 'OK'}, status=status.HTTP_201_CREATED)


class CodeforcesContestGetAPIView(generics.GenericAPIView):
    permission_classes = [AuthenticatedOrReadOnly]
    serializer_class = CodeforcesContestSerializer

    def get(self, request, handle, contestId):
        codeforcesUser = validate_handle(handle)
        if contestId == 0:
            contest = get_user_contests(codeforcesUser)
            if not contest.exists():
                return Response({'status': 'OK', 'result': {}})
            contest = contest[0]
        else:
            try:
                contest = CodeforcesContest.objects.get(id=contestId)
            except:
                raise ValidationException('contest id is invalid')
            if contest.owner != codeforcesUser:
                raise ValidationException('you are not allowed')

        contest_problem_qs = get_contest_problem_qs(contest)

        unixStartTime = contest.startTime - datetime(
            1970, 1, 1, tzinfo=timezone.utc)
        unixStartTime = unixStartTime.total_seconds()

        contest_problem_submission = codeforces_user_submissions(
            codeforcesUser, contest_problem_qs, unixStartTime)

        correct_probId = get_correct_submissions(
            submissions=contest_problem_submission)
        wrong_probId = get_wrong_submission(
            submissions=contest_problem_submission,
            SolvedProblems=correct_probId)

        return Response({
            'status':
            'OK',
            'result':
            CodeforcesContestSerializer(contest,
                                        context={
                                            'correct_probId':
                                            correct_probId,
                                            'wrong_probId':
                                            wrong_probId,
                                            'contest_problem_qs':
                                            contest_problem_qs
                                        }).data
        })


class CodeforcesProblemCheckAPIView(generics.GenericAPIView):
    permission_classes = [AuthenticatedOrReadOnly]
    serializer_class = CodeforcesContestSerializer

    def response(self, res):
        return Response({'status': 'OK', 'result': res})

    def get(self, request, handle, probId):
        codeforcesUser = validate_handle(handle)
        contest = get_user_contests(codeforcesUser)
        if not contest.exists():
            # No contest available for this user
            return self.response({})

        contest = contest[0]
        if datetime.now(tz=timezone.utc) > \
                        contest.startTime + timedelta(seconds= contest.duration):
            # No Contest is running at the moment
            return self.response({})

        contest_problem_qs = get_contest_problem_qs(contest)

        for prob in contest_problem_qs:
            similar_prob_qs = list(get_similar_problems(prob))
            similar_prob_qs.append(prob)
            for similar_prob in similar_prob_qs:
                if similar_prob.prob_id == probId:
                    return self.response(
                        MiniCodeforcesContestSerializer(contest).data)

        # No Problem is not in any running contest
        return self.response({})


# Costum Contest

# problem_rating = {
#     'div1': [(1600, 1900), (1900, 2100), (2100, 2300), (2300, 2400),
#              (2400, 2600), (2600, 2800), (2800, 3000), (3000, 3200),
#              (3200, 3400), (3400, 3600)],
#     'div2': [(800, 1000), (1000, 1200), (1200, 1600), (1600, 1900),
#              (1900, 2100), (2100, 2300), (2300, 2400), (2400, 2600),
#              (2600, 2800), (2800, 3000)],
#     'div3': [(800, 1000), (1000, 1200), (1200, 1400), (1400, 1500),
#              (1500, 1600), (1600, 1900), (1900, 2100), (2100, 2300),
#              (2300, 2400), (2400, 2600)],
#     'div4': [(800, 900), (900, 1100), (1100, 1200), (1200, 1400), (1400, 1500),
#              (1500, 1600), (1600, 1900), (1900, 2100), (2100, 2300),
#              (2300, 2400)]
# }

# # this will return a list of problem according to the contest
# # assign also
# # isProblem = true

# def get_mentor_problems(mentor_codeforces):
#     mentor_solved = set()

#     for mentor in mentor_codeforces:
#         try:
#             submissions_mentor = user_status(handle=mentor)
#         except ValidationException:
#             return mentor_solved
#         for submission in submissions_mentor:
#             if 'contestId' in submission['problem']:
#                 if submission['verdict'] == 'OK':
#                     mentor_solved.add(
#                         str(submission["problem"]['contestId']) +
#                         submission["problem"]['index'])
#     return mentor_solved

# def get_participant_problem(participants_codeforces):
#     participants_solved = set()

#     for participants in participants_codeforces:
#         try:
#             submissions_participant = user_status(handle=participants)
#         except ValidationException:
#             return participants_solved
#         for submission in submissions_participant:
#             if 'contestId' in submission['problem']:
#                 participants_solved.add(
#                     str(submission["problem"]['contestId']) +
#                     submission["problem"]['index'])
#     return participants_solved

# def makeContest(contest):

#     nProblems = request.POST.get('nProblems')
#     platforms = request.POST.get(
#         'platforms')  # TODO Till now  we are using only codeforces
#     tags = request.POST.get('tags')
#     rating = request.POST.get(
#         'rating')  # TODO We will take  count this too later
#     difficulty = request.POST.get('difficulty')
#     isMentorOn = request.POST.get('isMentorOn')
#     isGym = request.POST.get(
#         'isGym'
#     )  #TODO if false -> remove problems with -> platform='F' and len(contestId)>=6

#     participants = ContestParticipation.objects.filter(
#         contest=contest).values_list('user', flat=True)
#     participants_codeforces = list(
#         Profile.objects.filter(owner__in=participants).values_list(
#             'codeforces', flat=True))
#     participants_solved = get_participant_problem(participants_codeforces)

#     problems = Problem.objects.filter(platform='F')  # TODO all  platform

#     if isMentorOn:
#         mentor_codeforces = Profile.objects.get(
#             owner=contest.owner).gurus.split(',')[1:-1]
#         mentor_solved = get_mentor_problems(mentor_codeforces)
#         for ps in participants_solved:
#             if ps in mentor_solved:
#                 mentor_solved.remove(ps)

#     if isMentorOn and len(mentor_solved) > 10:
#         problems = problems.filter(prob_id__in=mentor_solved)
#     else:
#         problems = problems.exclude(prob_id__in=participants_solved)

#     if tags is not None:
#         tags = tags.split(',')
#         q = Q()
#         for tag in tags:
#             q |= Q(tags__icontains=tag)
#             problems = problems.filter(q)

#     # TODO more filter on problems  e.g. by TAG

#     # TODO Assuming  Div2 only

#     div = difficulty

#     nProblems = min(nProblems, problems.count())

#     for i in range(0, nProblems):

#         l, r = problem_rating[div][i]
#         newProblem = ContestProblem()
#         newProblem.contest = contest

#         while not problems.filter(rating__gte=l, rating__lt=r).exists():
#             l -= 100
#             r += 100
#             if l < 0:
#                 break

#         if problems.filter(rating__gte=l, rating__lt=r).exists():
#             newProblem.problem = problems.filter(rating__gte=l,
#                                                  rating__lt=r).order_by('?')[0]
#             newProblem.index = i
#             newProblem.save()

#     contest.isProblem = True
#     contest.save()
#     return

## Short Code Contest
# from .cron import update_codeforces_short_code_contests
# from .serializers import *

# def testing(requests):
# 	update_codeforces_short_code_contests()
# 	return JsonResponse({'status' :  'OK'})

# class ShortCodeContestAPIView(
#     mixins.CreateModelMixin,
#     generics.ListAPIView,
#     ):
# 	permission_classes = [AuthenticatedOrReadOnly]
# 	serializer_class = CodeforcesContestSerializer

# 	def get(self,request):
# 		shortCodeContest = CodeforcesContest.objects.filter(Type = 'Short Code')
# 		return JsonResponse({'status' : 'OK' , 'results' : CodeforcesContestSerializer(shortCodeContest, many=True).data})

# class ShortCodeContestStandingAPIView(
#     mixins.CreateModelMixin,
#     generics.ListAPIView,
#     ):
# 	permission_classes = [AuthenticatedOrReadOnly]
# 	serializer_class = CodeforcesContestParticipationSerializer

# 	def get(self,request,contestId):
# 		contest = CodeforcesContest.objects.filter(Type = 'Short Code' , contestId = contestId)
# 		if not contest.exists() :
# 			return JsonResponse({'status' :'FAILED' , 'error' : 'No such Contest Found'})

# 		participants = CodeforcesContestParticipation.objects.filter(contest = contest[0])
# 		return JsonResponse({
# 			'status' : 'OK',
# 			'results' : {
# 				'contest' : CodeforcesContestSerializer(contest, many=True).data,
# 				'standing' : CodeforcesContestParticipationSerializer(participants, many=True).data
# 			}
# 		})
