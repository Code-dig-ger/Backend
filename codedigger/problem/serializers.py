from rest_framework import serializers
from .models import Problem

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