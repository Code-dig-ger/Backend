from rest_framework import serializers

from .models import user,country,organization,contest ,user_contest_rank
from problem.models import Problem

class CountrySerializer(serializers.ModelSerializer):

    total = serializers.SerializerMethodField()

    def get_total(self , obj):
        return user.objects.filter(country = obj).count()

    class Meta:
        model = country
        fields = [
            'name',
            'total',
        ]

class OrganizationSerializer(serializers.ModelSerializer):

    total = serializers.SerializerMethodField()

    def get_total(self , obj):
        return user.objects.filter(organization = obj).count()

    class Meta:
        model = organization
        fields = [
            'name',
            'total',
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
    totalCountryParticipants = serializers.SerializerMethodField()
    totalOrganizationParticipants = serializers.SerializerMethodField()
    countryRank = serializers.SerializerMethodField()
    organizationRank = serializers.SerializerMethodField()

    def get_totalCountryParticipants(self , obj):
        cur_user = obj.user
        cur_contest = obj.contest
        cur_country = cur_user.country
        usersCountry = user.objects.filter(country = cur_country)
        usersCountryParticipation = user_contest_rank.objects.filter(user__in = usersCountry , contest = cur_contest)
        return usersCountryParticipation.count()

    def get_totalOrganizationParticipants(self , obj):
        cur_user = obj.user
        cur_contest = obj.contest
        cur_organization = cur_user.organization
        usersOrganization = user.objects.filter(organization = cur_organization)
        usersOrganizationParticipation = user_contest_rank.objects.filter(user__in = usersOrganization , contest = cur_contest)
        return usersOrganizationParticipation.count()

    def get_countryRank(self , obj):
        cur_user = obj.user
        cur_contest = obj.contest
        cur_country = cur_user.country
        usersCountry = user.objects.filter(country = cur_country)
        rank = user_contest_rank.objects.filter(user__in = usersCountry , contest = cur_contest , worldRank__lt = obj.worldRank).count()
        return rank+1

    def get_organizationRank(self , obj):
        cur_user = obj.user
        cur_contest = obj.contest
        cur_organization = cur_user.organization
        usersOrganization = user.objects.filter(organization = cur_organization)
        rank = user_contest_rank.objects.filter(user__in = usersOrganization , contest = cur_contest , worldRank__lt = obj.worldRank).count()
        return rank+1

    class Meta:
        model = user_contest_rank
        fields = [
            'contest',
            'worldRank',
            'countryRank',
            'organizationRank',
            'totalCountryParticipants',
            'totalOrganizationParticipants',
        ]

class UserSerializer():
    country = CountrySerializer()
    organization = OrganizationSerializer()
    
    contestRank = serializers.SerializerMethodField()
    worldRank = serializers.SerializerMethodField()
    countryRank = serializers.SerializerMethodField()
    organizationRank = serializers.SerializerMethodField()

    def get_worldRank(self , obj):
        return user.objects.filter(rating__gt = obj.rating).count()+1

    def get_countryRank(self, obj):
        if obj.country == None :
            return Nonserializers.ModelSerializere
        return user.objects.filter(rating__gt = obj.rating , country = obj.country).count()+1

    def get_organizationRank(self, obj):
        if obj.organization == None :
            return None
        return user.objects.filter(rating__gt = obj.rating , organization = obj.organization).count()+1

    def get_contestRank(self, obj):
        qs = user_contest_rank.objects.filter(user = obj)
        return contestRankSerializer(qs , many = True ).data

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
            'worldRank',
            'countryRank',
            'organizationRank',
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