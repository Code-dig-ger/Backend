from django.db import models
from django.db.models.deletion import CASCADE
from user.models import User
# Create your models here.
class Team(models.Model):
    name=models.CharField(max_length=100,blank=False)
    invite_code=models.CharField(max_length=50,unique=True,blank=False)
    owner=models.ForeignKey(User,
                            default=1,
                        on_delete=models.CASCADE,
                        related_name="owner")
    created_at=models.DateField(auto_now=True)
    members=models.ManyToManyField(User,
                                        through='teamMembers',
                                        through_fields=('team_id','user_id'),
                                        related_name='members')

    def __str__(self) -> str:
        return self.Team_name

class TeamMembers(models.Model):
    status=((True,'Invited'),(False,'Joined'))
    team_id=models.ForeignKey(Team,
                                on_delete=models.CASCADE,
                                related_name="Team_Id")
    user_id=models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='team_users')
    is_invited=models.BooleanField(choices=status)
    