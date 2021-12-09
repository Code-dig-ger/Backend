from django.db import models
from rest_framework import serializers, status
from .models import ListInfo, Solved, List, ListInfo, LadderStarted
from problem.models import Problem
from user.models import User, Profile
from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.core.paginator import Paginator
from django.db.models import Q, fields
from rest_framework.response import Response
from .solved_update import *
from user.exception import ValidationException
from django.template.defaultfilters import slugify


class ProblemSerializer(serializers.ModelSerializer):
    solved = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    platform = serializers.CharField(source='get_platform_display')

    def get_description(self, obj):
        slug = self.context.get("slug")
        qs = ListInfo.objects.filter(p_list=slug, problem=obj)
        if qs.exists():
            for ele in qs.values('description'):
                return ele['description']
        return " "

    def get_solved(self, obj):
        user = self.context.get("user")
        solve = Solved.objects.filter(user=user, problem=obj)
        return solve.exists()

    class Meta:
        model = Problem
        fields = (
            'id',
            'name',
            'prob_id',
            'url',
            'contest_id',
            'rating',
            'index',
            'tags',
            'platform',
            'difficulty',
            'editorial',
            'description',
            'solved',
        )


class GetSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    user_solved = serializers.SerializerMethodField()

    def get_total(self, attrs):
        return attrs.problem.count()

    def get_user_solved(self, attrs):
        cnt = 0
        user = self.context.get('user', None)
        if user is None or user.is_anonymous:
            return None
        for ele in attrs.problem.all():
            if Solved.objects.filter(user=user, problem=ele).exists():
                cnt += 1
        return cnt

    class Meta:
        model = List
        fields = ('id', 'name', 'description', 'total', 'user_solved', 'slug')


class GetLadderSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    user_solved = serializers.SerializerMethodField()
    first_time = serializers.SerializerMethodField()

    def get_total(self, attrs):
        return attrs.problem.count()

    def get_user_solved(self, attrs):
        cnt = 0
        user = self.context.get('user', None)
        if user is None or user.is_anonymous:
            return None
        for ele in attrs.problem.all():
            if Solved.objects.filter(user=user, problem=ele).exists():
                cnt += 1
        return cnt

    def get_first_time(self, attrs):
        user = self.context.get('user', None)
        if user is None or user.is_anonymous:
            return True
        if LadderStarted.objects.filter(ladder_user=user,
                                        ladder=attrs).exists():
            return False
        return True

    class Meta:
        model = List
        fields = ('id', 'name', 'description', 'total', 'user_solved',
                  'first_time', 'slug')


class GetUserlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ('id', 'name', 'description', 'slug', 'public')


class CreateUserlistSerializer(serializers.ModelSerializer):

    slug = serializers.SlugField(read_only=True)
    name = serializers.CharField(required=True)

    def validate_name(self, value):
        user = self.context.get('user')
        slug = slugify(value) + "-" + str(User.objects.get(username=user).id)
        if List.objects.filter(
                name=value,
                owner__username=user).exists() or List.objects.filter(
                    slug=slug, owner__username=user).exists():
            raise ValidationException(
                'List with the name or slug and user already exists')
        return value

    class Meta:
        model = List
        fields = ('id', 'name', 'description', 'slug', 'public')


class ProblemUserlisterializer(serializers.ModelSerializer):
    solved = serializers.SerializerMethodField()

    def get_solved(self, obj):
        user = self.context.get("user")
        solve = Solved.objects.filter(user__username=user, problem=obj)
        return solve.exists()

    class Meta:
        model = Problem
        fields = (
            'id',
            'name',
            'prob_id',
            'url',
            'contest_id',
            'rating',
            'index',
            'tags',
            'platform',
            'difficulty',
            'editorial',
            'solved',
        )


class EditUserlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = (
            'name',
            'description',
            'public',
        )


class UserlistAddSerializer(serializers.Serializer):
    prob_id = serializers.CharField(required=True)
    slug = serializers.CharField(required=True)
    platform = serializers.CharField(required=True)
    description = serializers.CharField(required=False)

    class Meta:
        fields = ('prob_id', 'slug', 'platform', 'description')


class UpdateLadderSerializer(serializers.Serializer):
    prob_id = serializers.CharField(required=True)

    class Meta:
        fields = ('prob_id', )


class UpdateListSerializer(serializers.Serializer):
    slug = serializers.CharField(required=True)
    page = serializers.CharField(required=True)

    class Meta:
        fields = (
            'slug',
            'page',
        )


class AddProblemsAdminSerializer(serializers.Serializer):
    slug = serializers.SlugField(required=True)

    class Meta:
        fields = ('slug', )