import http
# from telnetlib import STATUS
# from urllib import request
# from django.shortcuts import HttpResponse
from rest_framework import generics,status
from rest_framework.response import Response
from user.models import User
from user.response import response
from .serilaizers import TeamSerializers
from .models import Team,TeamMembers
import datetime,random,string 
# Create your views here.
class RegisterTeam(generics.GenericAPIView):
    seriliazer_class=TeamSerializers
    def post(self,request):
        team_data=request.data

        # serializers=self.seriliazer_class(data=team_data)
        
        # if serializers.is_valid():
        #     serializers.save()
        #     return response(serializers)
        # else:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)
        temp=''.join(random.choices(string.ascii_uppercase + string.digits+string.ascii_lowercase, k = 10))   
        team_object=Team.objects.create(
        name=team_data['name'],
        owner=request.user,
        created_at=datetime.date.today(),
        invite_code=temp 
        )
        team_object.save()
        team_member=TeamMembers.objects.create(
            user_id=request.user,
            team_id=team.objects.filter(invite_code__exact=temp).team_id
        )
        team_member.save()
        return response(team_data)

class TeamGetView(generics.ListAPIView):
    def get(self,request,user_id):
        Teams=TeamMembers.objects.filter(user_Id__exact=user_id)
        user_team=[Team.objects.filter(id__exact=team.Team_id) for team in Teams]
        return response(user_team)


