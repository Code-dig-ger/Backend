from datetime import timedelta, datetime, timezone
from rest_framework import serializers


# Models 
from .models import CodeforcesContest
from problem.models import Problem

# Serializers
from problem.serializers import MiniProblemSerializer

# Utily Functions
from .model_utils import get_contest_problem
from codeforces.codeforcesProblemSet import get_similar_problems


class MiniCodeforcesContestSerializer(serializers.ModelSerializer):
    isFinished = serializers.SerializerMethodField()
    
    def get_isFinished(self, obj):
        return True if datetime.now(tz=timezone.utc) > \
                        obj.startTime + timedelta(seconds= obj.duration)\
                    else False

    class Meta:
        model = CodeforcesContest
        fields = ['id', 'name', 'duration', 'startTime', 'isFinished']


class CodeforcesContestSerializer(serializers.ModelSerializer):
    
    isFinished = serializers.SerializerMethodField()
    problems = serializers.SerializerMethodField()
    
    def get_isFinished(self, obj):
        return True if datetime.now(tz=timezone.utc) > \
                        obj.startTime + timedelta(seconds= obj.duration)\
                    else False

    def get_problems(self, obj):
        correct_probId = self.context.get("correct_probId", set())
        wrong_probId = self.context.get("wrong_probId", set())
        contest_problem_qs = self.context.get("contest_problem_qs", [])

        problem_status = {}

        for prob in contest_problem_qs:

            similar_prob_qs = list(get_similar_problems(prob))
            similar_prob_qs.append(prob)

            for similar_prob in similar_prob_qs: 
                if similar_prob.prob_id in correct_probId:
                    problem_status[prob.prob_id] = 'SOLVED'
                
            for similar_prob in similar_prob_qs: 
                if similar_prob.prob_id in wrong_probId \
                        and prob.probId not in problem_status:
                    problem_status[prob.prob_id] = 'WRONG'
            
        return MiniProblemSerializer(contest_problem_qs, many=True, context = {
                            'problem_status': problem_status}).data

    class Meta:
        model = CodeforcesContest
        fields = ['id', 'name', 'duration', 'startTime', 'isFinished', 'problems']

# class CodeforcesContestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CodeforcesContest
#         fields = [
#             'name', 'contestId', 'groupId', 'Type', 'nproblems',
#             'showOnlyOfficial'
#         ]

# class CodeforcesContestSubmissionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CodeforcesContestSubmission
#         fields = [
#             'problemIndex', 'submissionId', 'isSolved', 'penalty', 'lang'
#         ]

# class CodeforcesContestParticipationSerializer(serializers.ModelSerializer):
#     user = MiniUserSerializer()
#     submissions = serializers.SerializerMethodField()

#     def get_submissions(self, obj):
#         qs = CodeforcesContestSubmission.objects.filter(participant=obj)
#         return CodeforcesContestSubmissionSerializer(qs, many=True).data

#     class Meta:
#         model = CodeforcesContestParticipation
#         fields = [
#             'participantId', 'isOfficial', 'isVirtual', 'user', 'submissions'
#         ]
