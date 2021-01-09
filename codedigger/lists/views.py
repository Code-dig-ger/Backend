from rest_framework import generics,status,permissions,views,response,mixins
from .models import ListInfo,Solved,List
from problem.models import Problem
from user.models import User,Profile
from .serializers import (
    GetLadderSerializer,
    GetSerializer,
    LadderRetrieveSerializer,
    RetrieveSerializer,
    GetUserlistSerializer,
    EditUserlistSerializer,
    CreateUserlistSerializer
)
from django.db.models import Q
from .permissions import IsOwner
from .solved_update import codeforces,uva,atcoder,codechef,spoj
from .cron import updater,cron_atcoder,cron_codechef,cron_codeforces,cron_spoj,cron_uva,codechef_list
from django.core.paginator import Paginator



class TopicwiseGetListView(generics.ListAPIView):
    serializer_class=GetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list = '1') | Q(type_list = '3')) & Q(isTopicWise = True) & Q(public=True))


class TopicWiseRetrieveView(generics.RetrieveAPIView):
    serializer_class = RetrieveSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list = '1') | Q(type_list = '3')) & Q(isTopicWise = True)  & Q(public=True))
    lookup_field = "slug"

    def get_serializer_context(self,**kwargs):
        data = super().get_serializer_context(**kwargs)
        data['user'] = self.request.user.username
        data['page'] = self.request.GET.get('page',None)
        return data


class TopicwiseGetLadderView(generics.ListAPIView):
    serializer_class=GetLadderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list = '2') | Q(type_list = '3')) & Q(isTopicWise = True)  & Q(public=True))


class TopicWiseLadderRetrieveView(generics.RetrieveAPIView):
    serializer_class = LadderRetrieveSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list = '2') | Q(type_list = '3')) & Q(isTopicWise = True) & Q(public=True))
    lookup_field = "slug"

    def get_serializer_context(self,**kwargs):
        data = super().get_serializer_context(**kwargs)
        data['user'] = self.request.user.username
        data['page'] = self.request.GET.get('page',None)
        data['logged_in'] = self.request.user.is_authenticated
        return data


class LevelwiseGetListView(generics.ListAPIView):
    serializer_class=GetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list = '1') | Q(type_list = '3')) & Q(isTopicWise = False)  & Q(public=True))


class LevelwiseRetrieveView(generics.RetrieveAPIView):
    serializer_class = RetrieveSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list = '1') | Q(type_list = '3')) & Q(isTopicWise = False)  & Q(public=True))
    lookup_field = "slug"

    def get_serializer_context(self,**kwargs):
        data = super().get_serializer_context(**kwargs)
        data['user'] = self.request.user.username
        data['page'] = self.request.GET.get('page',None)
        return data


class LevelwiseGetLadderView(generics.ListAPIView):
    serializer_class=GetLadderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list = '2') | Q(type_list = '3')) & Q(isTopicWise = False)  & Q(public=True))


class LevelwiseLadderRetrieveView(generics.RetrieveAPIView):
    serializer_class = LadderRetrieveSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = List.objects.filter((Q(type_list = '2') | Q(type_list = '3')) & Q(isTopicWise = False)  & Q(public=True))
    lookup_field = "slug"

    def get_serializer_context(self,**kwargs):
        data = super().get_serializer_context(**kwargs)
        data['user'] = self.request.user.username
        data['page'] = self.request.GET.get('page',None)
        data['logged_in'] = self.request.user.is_authenticated
        return data


class updateLadderview(views.APIView):
    def get(self,request,*args, **kwargs):
        prob_id = self.request.GET.get('prob_id')
        if prob_id == None:
            codeforces(self.request.user.username)
            uva(self.request.user.username)
            atcoder(self.request.user.username)
        else:
            if Problem.objects.filter(prob_id=prob_id,platform='F').exists():
                codeforces(self.request.user.username)
            if Problem.objects.filter(prob_id=prob_id,platform='U').exists():
                uva(self.request.user.username)
            if Problem.objects.filter(prob_id=prob_id,platform='A').exists():
                atcoder(self.request.user.username)
            if Problem.objects.filter(prob_id=prob_id,platform='C').exists():
                codechef(self.request.user.username,prob_id)
            if Problem.objects.filter(prob_id=prob_id,platform='S').exists():
                spoj(self.request.user.username,prob_id)
        return response.Response(data={'status' : 'ok'})

class updateListView(views.APIView):
    def get(self,request,*args,**kwargs):
        list_slug = self.request.GET.get('slug')
        page = self.request.GET.get('page')
        if list_slug is None or list_slug == "" :
            return response.Response(data={'status' : 'No list provided'})
        if page is None or page == "":
            return response.Response(data={'status' : 'No page provided'})
        curr_list = List.objects.get(slug=list_slug)
        #set page size here and in the serializer list waala
        page_size = 6
        paginator = Paginator(curr_list.problem.all(),page_size)
        qs = paginator.page(page)  
        check = {'S' : set(),'U' : 0,'C' : set(),'F' : 0,'A' : 0}
        for prob in qs:
            platform = prob.platform
            if not Solved.objects.filter(user=self.request.user,problem__prob_id=prob.prob_id).exists():
                if platform == 'S' or platform == 'C':
                    check[platform].add(prob.prob_id)
                else:
                    check[platform] += 1
        print(check)
        if check['F'] > 0:
            cron_codeforces(self.request.user.username) 
        if check['U'] > 0:
            cron_uva(self.request.user.username)
        if check['A'] > 0:
            cron_atcoder(self.request.user.username)
        if len(check['S']) > 0:
            for item in check['S']:
                spoj(self.request.user.username,item)
        if len(check['C']) > 0:
            list1 = codechef_list(self.request.user.username)
            list2 = check['C']
            final = set((list1) & (list2))
            for ele in final:
                prob = Problem.objects.get(prob_id=ele,platform='C')
                user = self.request.user
                Solved.objects.create(user=user,problem=prob)
        return response.Response(data={'status' : 'ok'})


class UserlistGetView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetUserlistSerializer
    
    def get_queryset(self):
        qs = List.objects.filter(owner=self.request.user)
        return qs
    

class UserlistCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateUserlistSerializer

    def get_serializer_context(self,**kwargs):
        data = super().get_serializer_context(**kwargs)
        data['user'] = self.request.user.username
        return data

    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)


class UserlistAddProblemView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,*args, **kwargs):
        data = request.data
        prob_id = data.get('prob_id',None)
        slug = data.get('slug',None)
        if prob_id is None or slug is None:
            return response.Response({"status" : "prob_id or slug or both not provided"},status=status.HTTP_400_BAD_REQUEST)
        if not List.objects.filter(slug = slug).exists():
            return response.Response({"status" : "List with the provided slug does not exist"},status=status.HTTP_400_BAD_REQUEST)
        if not Problem.objects.filter(prob_id = prob_id).exists():
            return response.Response({"status" : "Problem with the given prob_id does not exist"},status=status.HTTP_400_BAD_REQUEST)
        curr_list = List.objects.get(slug=slug)
        curr_prob = Problem.objects.get(prob_id=prob_id)
        if curr_list.problem.filter(prob_id=prob_id).exists():
            return response.Response({"status" : "Problem with the given prob_id already exists within the list"},status=status.HTTP_400_BAD_REQUEST)
        curr_list.problem.add(curr_prob)
        return response.Response({"status" : "Given problem has been added to the list"},status = status.HTTP_200_OK)


class EditUserlistView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EditUserlistSerializer
    queryset = List.objects.all()
    lookup_field = 'slug'

    def get_serializer_context(self,**kwargs):
        data = super().get_serializer_context(**kwargs)
        data['user'] = self.request.user.username
        return data

    def update(self,request,**kwargs):
        data = request.data
        if data.get('prob_id',None):
            for ele in data.get('prob_id',None):
                if not Problem.objects.filter(prob_id = ele).exists():
                    return response.Response({"status" : "Problem with the prob_id " + ele + " does not exist"},status=status.HTTP_400_BAD_REQUEST) 
                if not List.objects.filter(slug = data['slug']).exists():
                    return response.Response({"status" : "List with the provided slug does not exist"},status=status.HTTP_400_BAD_REQUEST)
                curr_prob = Problem.objects.get(prob_id=ele)
                curr_list = List.objects.get(slug=data['slug'])
                if not curr_list.problem.filter(prob_id=ele).exists():
                    return response.Response({"status" : "Problem with the given prob_id " + ele + " does not exists within the list"},status=status.HTTP_400_BAD_REQUEST) 
                curr_list.problem.remove(curr_prob)
        return super().update(request,**kwargs)