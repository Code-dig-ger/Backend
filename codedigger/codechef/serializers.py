from rest_framework import serializers
from problem.models import Problem
from codechef.models import CodechefContest, CodechefContestProblems
from problem.serializers import CCUpsolveContestSerializer, ProbSerializer


class CodechefUpsolveSerializer(serializers.ModelSerializer):

    problems = serializers.SerializerMethodField()

    def get_problems(self, obj):
        context = {
            'upsolved': self.context.get('upsolved'),
            'solved': self.context.get('solved')
        }
        pr = Problem.objects.filter(
            codechefcontestproblems__in=CodechefContestProblems.objects.filter(
                contest=obj))
        return CCUpsolveContestSerializer(pr, many=True, context=context).data

    class Meta:
        model = CodechefContest

        fields = [
            'name',
            'contestId',
            'duration',
            'startTime',
            'problems',
        ]
