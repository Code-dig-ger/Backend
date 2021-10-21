from rest_framework import serializers

from .models import user, country, organization, contest, user_contest_rank
from problem.models import Problem
from problem.serializers import UpsolveProblemsSerializer


class CountrySerializer(serializers.ModelSerializer):

    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        return user.objects.filter(country=obj).count()

    class Meta:
        model = country
        fields = [
            'name',
            'total',
        ]


class OrganizationSerializer(serializers.ModelSerializer):

    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        return user.objects.filter(organization=obj).count()

    class Meta:
        model = organization
        fields = [
            'name',
            'total',
        ]


class ContestSerializer(serializers.ModelSerializer):
    Type = serializers.CharField(source='get_Type_display')
    participants = serializers.SerializerMethodField()

    def get_participants(self, obj):
        return user_contest_rank.objects.filter(contest=obj).count()

    class Meta:
        model = contest
        fields = [
            'name', 'contestId', 'duration', 'startTime', 'Type',
            'participants'
        ]


class contestRankSerializer(serializers.ModelSerializer):
    contest = ContestSerializer()
    totalCountryParticipants = serializers.SerializerMethodField()
    totalOrganizationParticipants = serializers.SerializerMethodField()
    countryRank = serializers.SerializerMethodField()
    organizationRank = serializers.SerializerMethodField()

    def get_totalCountryParticipants(self, obj):
        if obj.user.country == None:
            return None
        return user_contest_rank.objects.filter(
            user__in=user.objects.filter(country=obj.user.country),
            contest=obj.contest).count()

    def get_totalOrganizationParticipants(self, obj):
        if obj.user.organization == None:
            return None
        return user_contest_rank.objects.filter(
            user__in=user.objects.filter(organization=obj.user.organization),
            contest=obj.contest).count()

    def get_countryRank(self, obj):
        if obj.user.country == None:
            return None
        return user_contest_rank.objects.filter(
            user__in=user.objects.filter(country=obj.user.country),
            contest=obj.contest,
            worldRank__lt=obj.worldRank).count() + 1

    def get_organizationRank(self, obj):
        if obj.user.organization == None:
            return None
        return user_contest_rank.objects.filter(
            user__in=user.objects.filter(organization=obj.user.organization),
            contest=obj.contest,
            worldRank__lt=obj.worldRank).count() + 1

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


class UserSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    organization = OrganizationSerializer()

    totalUsers = serializers.SerializerMethodField()
    contestRank = serializers.SerializerMethodField()
    worldRank = serializers.SerializerMethodField()
    countryRank = serializers.SerializerMethodField()
    contestCount = serializers.SerializerMethodField()
    organizationRank = serializers.SerializerMethodField()

    def get_totalUsers(self, obj):
        return user.objects.all().count()

    def get_worldRank(self, obj):
        return user.objects.filter(rating__gt=obj.rating).count() + 1

    def get_countryRank(self, obj):
        if obj.country == None:
            return None
        return user.objects.filter(rating__gt=obj.rating,
                                   country=obj.country).count() + 1

    def get_organizationRank(self, obj):
        if obj.organization == None:
            return None
        return user.objects.filter(rating__gt=obj.rating,
                                   organization=obj.organization).count() + 1

    def get_contestCount(self, obj):
        return user_contest_rank.objects.filter(user=obj).count()

    def get_contestRank(self, obj):
        qs = user_contest_rank.objects.filter(
            user=obj).order_by('worldRank')[:3]
        return contestRankSerializer(qs, many=True).data

    class Meta:
        model = user
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
            'totalUsers',
            'worldRank',
            'countryRank',
            'organizationRank',
            'contestCount',
            'contestRank',
        ]


class MiniUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user

        fields = ['name', 'handle', 'rating', 'rank', 'photoUrl']



class CodeforcesUpsolveSerializer(serializers.ModelSerializer):

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
