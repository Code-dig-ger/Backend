from rest_framework import serializers
from problem.models import Problem
from codechef.models import CodechefContest, CodechefContestProblems
from problem.serializers import ProbSerializer


class CodechefUpsolveSerializer(serializers.ModelSerializer):

    problems = serializers.SerializerMethodField()
        
    def get_problems(self, obj):

        pr = Problem.objects.filter(codechefcontestproblems__in=CodechefContestProblems.objects.filter(contest=obj))
        return ProbSerializer(pr, many=True).data

    class Meta:
        model = CodechefContest

        fields = [
            'name',
            'contestId',
            'duration',
            'startTime',
            'problems',
        ]