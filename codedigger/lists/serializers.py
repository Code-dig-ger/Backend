from rest_framework import serializers,status
from .models import ListInfo,Solved,List,ListInfo
from problem.models import Problem
from user.models import User,Profile
from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.response import Response
from .solved_update import *

class ProblemSerializer(serializers.ModelSerializer):
    solved = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    def get_description(self,obj):
        slug = self.context.get("slug")
        qs = ListInfo.objects.filter(p_list__slug = slug,problem = obj)
        if qs.exists():
            for ele in qs.values('description'):
                return ele['description']
        return " "


    def get_solved(self,obj):
        user = self.context.get("user")
        solve = Solved.objects.filter(user__username=user,problem = obj)
        return solve.exists()



    class Meta:
        model = Problem
        fields = ('id','name','prob_id','url','contest_id','rating','index','tags','platform','difficulty','editorial','description','solved',)

class GetSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = ('id','name','description','slug')


class GetLadderSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = ('id','name','description','slug',)


class GetUserlistSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = ('id','name','description','slug','public')

class CreateUserlistSerializer(serializers.ModelSerializer):

    slug = serializers.SlugField(read_only=True)
    name = serializers.CharField(required=True)

    def validate_name(self,value):
        user = self.context.get('user')
        if List.objects.filter(name=value,owner__username=user).exists():
            raise serializers.ValidationError('List with the name and user already exists')
        return value


    class Meta:
        model = List
        fields = ('id','name','description','slug','public')


class ProblemUserlisterializer(serializers.ModelSerializer):
    solved = serializers.SerializerMethodField()

    def get_solved(self,obj):
        user = self.context.get("user")
        solve = Solved.objects.filter(user__username=user,problem = obj)
        return solve.exists()

    class Meta:
        model = Problem
        fields = ('id','name','prob_id','url','contest_id','rating','index','tags','platform','difficulty','editorial','solved',)

class EditUserlistSerializer(serializers.ModelSerializer):
    problem = serializers.SerializerMethodField()

    def get_problem(self,attrs):
        user = self.context.get('user')
        return ProblemSerializer(attrs.problem.all(),many=True,context = {"user" : user}).data

    class Meta:
        model = List
        fields = ('id','name','description','problem','slug','public')


class UserlistAddSerializer(serializers.Serializer):
    prob_id = serializers.CharField(required=True)
    slug = serializers.CharField(required=True)

    class Meta:
        fields = ('prob_id','slug')

class UpdateLadderSerializer(serializers.Serializer):
    prob_id = serializers.CharField(required=True)

    class Meta:
        fields = ('prob_id',)

class UpdateListSerializer(serializers.Serializer):
    slug = serializers.CharField(required=True)
    page = serializers.IntegerField(required=True)

    class Meta:
        fields = ('slug','page',)