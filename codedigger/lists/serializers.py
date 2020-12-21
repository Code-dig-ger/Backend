from rest_framework import serializers
from .models import ListInfo,Solved,List,ListInfo
from problem.models import Problem
from user.models import User
from drf_writable_nested.serializers import WritableNestedModelSerializer


class ProblemSerializer(serializers.ModelSerializer):
    solved = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    def get_description(self,obj):
        curr_list = self.context["list"]
        qs = ListInfo.objects.filter(problem=obj,curr_list__name=curr_list)
        if qs.exists():
            return qs.desciption
        return " "



    def get_solved(self,obj):
        user = self.context["user"]
        solve = Solved.objects.filter(user__username=user,problem = obj)
        if solve.exists():
            return True
        return False



    class Meta:
        model = Problem
        fields = ('id','name','prob_id','url','contest_id','rating','index','tags','platform','difficulty','editorial','description','solved')

class TopicwiseGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = ('id','name','description',)


class TopicwiseRetrieveSerializer(WritableNestedModelSerializer):
    user = serializers.SerializerMethodField()
    problem = ProblemSerializer(many = True,context = {'user' : user,'list' : })
    def get_user(self,attrs):
        user = self.context.get('user')
        return user

    class Meta:
        model = List
        fields = ('id','user','name','description','problem',)
    