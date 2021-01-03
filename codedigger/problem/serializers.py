from rest_framework import serializers
from .models import Problem
from codeforces.models import contest ,user_contest_rank

class ProbSerializer(serializers.ModelSerializer):

    platform = serializers.CharField(source='get_platform_display')
    difficulty = serializers.CharField(source='get_difficulty_display') 
    class Meta:
        model= Problem
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
            'editorial'
        ]

class UpsolveProblemsSerializer(serializers.ModelSerializer):

    platform = serializers.CharField(source='get_platform_display')
    difficulty = serializers.CharField(source='get_difficulty_display') 
    status = serializers.SerializerMethodField()

    def get_status(self , obj):

        if obj.prob_id in self.context.get('solved') :
            return 'solved'
        elif obj.prob_id in self.context.get('upsolved') :
            return 'upsolved'
        elif obj.prob_id in self.context.get('wrong') :
            return 'wrong'
        else :
            return 'not_attempt'

    class Meta:
        model= Problem
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

    Type = serializers.CharField(source='get_Type_display') 
    problems = serializers.SerializerMethodField()

    def get_problems(self , obj):
        context = {
            'wrong' : self.context.get('wrong') , 
            'upsolved' : self.context.get('upsolved') ,
            'solved' : self.context.get('solved') 
        }
        pr = Problem.objects.filter(contest_id = obj.contestId).order_by('index')
        return UpsolveProblemsSerializer(pr , many = True , context = context).data

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

    class Meta:
        model= Problem
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
        ]

class SolveProblemsSerializer(serializers.ModelSerializer): 
    tags = serializers.ListField()
    mentors=serializers.BooleanField()
    class Meta:
        model = Problem
        fields = ['tags','mentors']