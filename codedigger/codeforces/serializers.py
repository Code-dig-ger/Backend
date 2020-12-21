from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from .models import user,country,organization,contest ,user_contest_rank
from .models import organization_contest_participation, country_contest_participation

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = country
        fields = [
            'name',
            'total'
        ]

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = organization
        fields = [
            'name',
            'total'
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
            'participants',
            'Type'
        ]

class contestRankSerializer(serializers.ModelSerializer):
    contest = ContestSerializer()
    class Meta:
        model = user_contest_rank
        fields = [
            'contest',
            'worldRank',
            'countryRank',
            'organizationRank'
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
            'worldRank',
            'countryRank',
            'organizationRank',
            'country',
            'organization',
            'photoUrl',
            'contestRank',
        ]