from rest_framework import serializers

from .models import user,country,organization,contest ,user_contest_rank

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = country
        fields = [
            'name',
        ]

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = organization
        fields = [
            'name',
        ]

class ContestSerializer(serializers.ModelSerializer):
    Type = serializers.CharField(source='get_Type_display') 
    class Meta:
        model = contest
        fields = [
            'name',
            'contestId',
            'duration',
            'startTime',
            'Type'
        ]

class contestRankSerializer(serializers.ModelSerializer):
    contest = ContestSerializer()
    class Meta:
        model = user_contest_rank
        fields = [
            'contest',
            'worldRank'
        ]

class UserSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    organization = OrganizationSerializer()
    contestRank = ContestSerializer( many = True)
    
    class Meta:
        model= user
        fields = [
            'name',
            'handle',
            'rating',
            'maxRating',
            'rank',
            'maxRank',
            'country',
            'organization',
            'photoUrl',
            'contestRank',
        ]