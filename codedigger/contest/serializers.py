from datetime import timedelta, datetime, timezone
from rest_framework import serializers

# Models 
from .models import CodeforcesContest
from problem.models import Problem

# Serializers
from problem.serializers import MiniProblemSerializer

# Utily Functions
from .model_utils import get_contest_problem


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
        contest_problem_qs = get_contest_problem(obj)     
        problem_qs = []
        for id in contest_problem_qs:
            problem_qs.append(Problem.objects.get(id = id))
        # TODO pass which prob_id is solved, wrong, not attempt
        return MiniProblemSerializer(problem_qs, many=True).data

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
