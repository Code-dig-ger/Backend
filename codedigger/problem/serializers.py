from re import S
from rest_framework import serializers

from codeforces.models import contest
from lists.models import Solved

from .models import Problem, DIFFICULTY


class MiniProblemSerializer(serializers.ModelSerializer):

    platform = serializers.CharField(source='get_platform_display')
    type = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_type(self, obj):
        if obj.platform == 'F' and 'gym' in obj.url:
            return 'gym'
        else:
            return 'contest'

    def get_status(self, obj):
        problem_status = self.context.get("problem_status", {})
        return problem_status.get(obj.prob_id, "NOT_ATTEMPT")

    class Meta:
        model = Problem
        fields = [
            'name', 'url', 'prob_id', 'contest_id', 'index', 'platform',
            'type', 'status'
        ]


class ProbSerializer(serializers.ModelSerializer):

    platform = serializers.CharField(source='get_platform_display')
    difficulty = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    solved = serializers.SerializerMethodField()

    def get_rating(self, obj):
        if obj.rating == None or \
            (obj.rating % 100 != 0 and obj.platform != 'A'):
            return None
        return obj.rating

    def get_difficulty(self, obj):
        if obj.difficulty != None and obj.difficulty != "" and \
            (obj.platform == 'C' or obj.rating == None or \
              obj.rating % 100 == 0 or obj.platform == 'A') :
            return dict(DIFFICULTY)[obj.difficulty]
        else:
            return None

    def get_solved(self, obj):
        user = self.context.get("user", None)
        solve = Solved.objects.filter(user=user, problem=obj)
        return solve.exists()

    class Meta:
        model = Problem
        fields = [
            'name', 'url', 'prob_id', 'tags', 'contest_id', 'rating', 'index',
            'platform', 'difficulty', 'editorial', 'solved'
        ]


class UpsolveProblemsSerializer(serializers.ModelSerializer):

    platform = serializers.CharField(source='get_platform_display')
    difficulty = serializers.CharField(source='get_difficulty_display')
    status = serializers.SerializerMethodField()

    def get_status(self, obj):

        if obj.prob_id in self.context.get('solved'):
            return 'solved'
        elif obj.prob_id in self.context.get('upsolved'):
            return 'upsolved'
        elif obj.prob_id in self.context.get('wrong'):
            return 'wrong'
        else:
            return 'not_attempt'

    class Meta:
        model = Problem
        fields = [
            'name',
            'url',
            'prob_id',
            'tags',
            'contest_id',
            'rating',
            'index',
            'platform',
            'difficulty',
            'editorial',
            'status',
        ]


class UpsolveContestSerializer(serializers.ModelSerializer):
    # Deprecated

    Type = serializers.CharField(source='get_Type_display')
    problems = serializers.SerializerMethodField()

    def get_problems(self, obj):
        context = {
            'wrong': self.context.get('wrong'),
            'upsolved': self.context.get('upsolved'),
            'solved': self.context.get('solved')
        }
        pr = Problem.objects.filter(contest_id=obj.contestId).order_by('index')
        return UpsolveProblemsSerializer(pr, many=True, context=context).data

    class Meta:
        model = contest
        fields = [
            'name',
            'contestId',
            'duration',
            'startTime',
            'Type',
            'problems',
        ]


class CCUpsolveContestSerializer(serializers.ModelSerializer):

    status = serializers.SerializerMethodField()

    def get_status(self, obj):

        if obj.prob_id in self.context.get('solved'):
            return 'solved'
        elif obj.prob_id in self.context.get('upsolved'):
            return 'upsolved'
        else:
            return 'not_attempt'

    class Meta:
        model = Problem
        fields = [
            'name', 'url', 'prob_id', 'tags', 'contest_id', 'rating', 'index',
            'platform', 'difficulty', 'editorial', 'status'
        ]


class SolveProblemsSerializer(serializers.ModelSerializer):
    tags = serializers.ListField()
    mentors = serializers.BooleanField()

    class Meta:
        model = Problem
        fields = ['tags', 'mentors']
