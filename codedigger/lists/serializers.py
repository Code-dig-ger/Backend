from rest_framework import serializers,status
from .models import ListInfo,Solved,List,ListInfo
from problem.models import Problem
from user.models import User,Profile
from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.response import Response

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
        fields = ('id','name','description','slug')

limit_list = None

def get_limit_list():
    global limit_list
    return limit_list

def change_limit_list(x):
    global limit_list
    limit_list = x

list_page_size = 2
class RetrieveSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    problem = serializers.SerializerMethodField()
    page = serializers.SerializerMethodField()
    prev_page = serializers.SerializerMethodField()
    next_page = serializers.SerializerMethodField()


    def get_user(self,attrs):
        user = self.context.get('user')
        return user


    def get_problem(self,attrs):
        user = self.context.get('user')
        name = attrs.name
        page = self.context.get('page')
        page_size = list_page_size
        paginator = Paginator(attrs.problem.all(),page_size)
        cnt = int(attrs.problem.all().count()/page_size)
        if attrs.problem.all().count() % page_size != 0:
            cnt += 1
        change_limit_list(cnt)
        if page == None:
            qs = paginator.page(1)
            return ProblemSerializer(qs,many = True,context = {"name" : name,"user" : user}).data
        else:
            qs = paginator.page(int(page))
            return ProblemSerializer(qs,many=True,context = {"name" : name,"user" : user}).data

    def get_page(self,obj):
        page = self.context.get('page')
        if page is None:
            return 1
        return int(page)
    
    def get_prev_page(self,obj):
        page = self.context.get('page')
        if page is None:
            return None
        else:
            if int(page) == 1:
                return None
            return int(page)-1

    def get_next_page(self,obj):
        page = self.context.get('page')
        if page is None:
            return 2
        else:
            if int(page) ==get_limit_list():
                return None
            return int(page)+1

    class Meta:
        model = List
        fields = ('id','user','name','description','problem','page','next_page','prev_page','slug',)
        change_limit_list(None)
    

class GetLadderSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = ('id','name','description','slug',)

curr_prob = None
def get_curr_prob():
    global curr_prob
    return curr_prob

def change_curr_prob(x):
    global curr_prob
    curr_prob=x


limit_ladder = None
def get_ladder():
    global limit_ladder
    return limit_ladder

def change_ladder(x):
    global limit_ladder
    limit_ladder = x

curr_page = 1
def get_curr_page():
    global curr_page
    return curr_page

def change_page(x):
    global curr_page
    curr_page = x


ladder_page_size = 1

class LadderRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    problem = serializers.SerializerMethodField()
    page = serializers.SerializerMethodField()
    prev_page = serializers.SerializerMethodField()
    next_page = serializers.SerializerMethodField()
    curr_prob = serializers.SerializerMethodField()


    def get_user(self,attrs):
        user = self.context.get('user')
        return user

    def get_problem(self,attrs):
        user = self.context.get('user')
        page = self.context.get('page')
        logged_in = self.context.get('logged_in')
        name = attrs.name
        page_size = ladder_page_size
        qs = attrs.problem.all()
        if logged_in:
            spoj = Profile.objects.get(owner__username = user).spoj
            uva = Profile.objects.get(owner__username = user).uva_handle
            codeforces = Profile.objects.get(owner__username = user).codeforces
            codechef = Profile.objects.get(owner__username = user).codechef
            atcoder = Profile.objects.get(owner__username = user).atcoder
            temp = []
            if spoj is None:
                temp.append('S')
            if uva is None:
                temp.append('U')
            if atcoder is None:
                temp.append('A')
            if codechef is None:
                temp.append('C')
            final = None
            prev = None
            for ele in temp:
                if prev is None:
                    prev = qs.exclude(platform=ele)
                    final = prev
                else:
                    chain1 = prev.exclude(platform=ele)
                    prev = chain1
                    final = prev
            if final is None:
                paginator = Paginator(qs,page_size)
                cnt = (int)(qs.count()/ladder_page_size)
                if qs.count() % ladder_page_size != 0:
                    cnt += 1
                change_ladder(cnt)
                if page == None:
                    page = 1
                    while page <= get_ladder():
                        qs = paginator.page(page)
                        for ele in qs:
                            solve = Solved.objects.filter(user__username=user,problem=ele)
                            if not solve.exists():
                                change_page(page)
                                change_curr_prob(ele.prob_id)
                                return ProblemSerializer(qs,many=True,context = {"name" : name,"user" : user}).data
                        page += 1
                else:
                    qs = paginator.page(int(page))
                    return ProblemSerializer(qs,many=True,context = {"name" : name,"user" : user}).data
            else:
                paginator = Paginator(final,page_size)
                cnt = (int)(final.count()/ladder_page_size)
                if final.count() % ladder_page_size != 0:
                    cnt += 1
                change_ladder(cnt)
                if page == None:
                    page = 1
                    while page <= get_ladder():
                        qs = paginator.page(page)
                        for ele in qs:
                            solve = Solved.objects.filter(user__username=user,problem=ele)
                            if not solve.exists():
                                change_page(page)
                                print(ele.prob_id)
                                change_curr_prob(ele.prob_id)
                                return ProblemSerializer(qs,many=True,context = {"name" : name,"user" : user}).data
                        page += 1
                else:
                    qs = paginator.page(int(page))
                    return ProblemSerializer(qs,many=True,context = {"name" : name,"user" : user}).data
        else:
            paginator = Paginator(qs,page_size)
            cnt = (int)(qs.count()/ladder_page_size)
            if qs.count() % ladder_page_size != 0:
                cnt += 1
            change_ladder(cnt)
            if page == None:
                page = 1
                qs = paginator.page(int(page))
                return ProblemSerializer(qs,many=True,context = {"name" : name,"user" : user}).data
            else:
                qs = paginator.page(int(page))
                return ProblemSerializer(qs,many=True,context = {"name" : name,"user" : user}).data

    
    def get_page(self,obj):
        page = self.context.get('page')
        if page is None:
            return get_curr_page()
        return int(page)
    
    def get_prev_page(self,obj):
        page = self.context.get('page')
        if page is None:
            page = get_curr_page()
            if page == 1:
                return None
            return page-1
        else:
            page = int(page)
            if page == 1:
                return None
            return page-1

    def get_next_page(self,obj):
        page = self.context.get('page')
        if page is None:
            page = get_curr_page()
            if page == get_ladder():
                return None
            return page+1
        else:
            page = int(page)
            if page == get_ladder():
                return None
            return page+1

    def get_curr_prob(self,obj):
        return get_curr_prob()
        

    class Meta:
        model = List
        fields = ('id','user','name','description','problem','curr_prob','page','next_page','prev_page','slug',)
        change_ladder(None)
        change_page(1)
        change_curr_prob(None)