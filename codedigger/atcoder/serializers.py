from rest_framework import serializers
from problem.models import Problem, atcoder_contest

class AtcoderProblemSerializer(serializers.ModelSerializer):

    status = serializers.SerializerMethodField()

    def get_status(self, obj):

        if obj.prob_id in self.context.get('solved'):
            return 'solved'
        elif obj.prob_id in self.context.get('wrong'):
            return 'wrong'
        else:
            return 'not_attempt'

    class Meta:
        model = Problem
        fields = [
            'name', 'url', 'prob_id', 'tags', 'contest_id', 'rating', 'index',
            'platform', 'difficulty', 'editorial', 'status'
        ]


class AtcoderUpsolveContestSerializer(serializers.ModelSerializer):

    problems = serializers.SerializerMethodField()

    def get_problems(self, obj):
        qs = Problem.objects.filter(platform='A',
                                    contest_id=obj.contestId).order_by('index')
        return AtcoderProblemSerializer(qs,
                                        many=True,
                                        context={
                                            'solved':
                                            self.context.get('solved'),
                                            'wrong': self.context.get('wrong')
                                        }).data

    class Meta:

        model = atcoder_contest
        fields = ['name', 'contestId', 'startTime', 'duration', 'problems']
