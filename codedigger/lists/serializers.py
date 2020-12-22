from rest_framework import serializers
from .models import ListInfo,Solved,List,ListInfo
from problem.models import Problem
from user.models import User
from drf_writable_nested.serializers import WritableNestedModelSerializer

class ProblemSerializer(serializers.ModelSerializer):
    solved = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    def get_description(self,obj):
        name = self.context.get("name")
        qs = ListInfo.objects.filter(l__name = name,problem = obj)
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
        fields = ('id','name','prob_id','url','contest_id','rating','index','tags','platform','difficulty','editorial','description','solved')

class TopicwiseGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = ('id','name','description',)


class TopicwiseRetrieveSerializer(WritableNestedModelSerializer):
    user = serializers.SerializerMethodField()
    problem = serializers.SerializerMethodField()
    
    def get_user(self,attrs):
        user = self.context.get('user')
        return user


    def get_problem(self,attrs):
        user = self.context.get('user')
        name = attrs.name
        qs = attrs.problem.all()
        return ProblemSerializer(qs,many = True,context = {"name" : name,"user" : user}).data

    class Meta:
        model = List
        fields = ('id','user','name','description','problem',)
    