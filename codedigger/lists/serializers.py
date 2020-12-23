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
        qs = ListInfo.objects.filter(p_list__name = name,problem = obj)
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

class GetSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = ('id','name','description',)


class RetrieveSerializer(serializers.ModelSerializer):
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
    

class GetLadderSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = ('id','name','description',)

class LadderRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    problem = serializers.SerializerMethodField()
    
    def get_user(self,attrs):
        user = self.context.get('user')
        return user

    def get_problem(self,attrs):
        cnt = 0
        user = self.context.get('user')
        name = attrs.name
        while cnt <= 3:
            for qs in attrs.problem.all()[cnt:cnt+2]
                
        # for qs in attrs.problem.all():
        #     solve = Solved.objects.filter(user__username=user,problem=qs)
        #     cnt += 1
        #     if not solve.exists():
        #         return ProblemSerializer(qs[cnt:cnt+2],many=True,context = {"name" : name,"user" : user}).data
        qs = attrs.problem.all()
        return ProblemSerializer(qs,many = True,context = {"name" : name,"user" : user}).data

    class Meta:
        model = List
        fields = ('id','user','name','description','problem',)