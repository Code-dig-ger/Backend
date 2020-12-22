from django.db import models
from problem.models import Problem
from user.models import User


TYPE_CHOICES = (
    ("1" , "List"),
    ("2" , "Ladder"),
    ("3" , "Both"),
)

class List(models.Model):
    owner = models.ForeignKey(to=User,on_delete=models.CASCADE)
    problem = models.ManyToManyField(Problem,related_name='problem')
    name = models.CharField(max_length=255,default=" ")
    description = models.TextField(max_length=400,default=" ")
    isAdmin = models.BooleanField(default=True)
    isTopicWise = models.BooleanField(default=True)
    type_list = models.CharField(max_length=10,choices=TYPE_CHOICES,default='1')

    def __str__(self):
        return self.name
    

class ListInfo(models.Model):   
    l = models.ForeignKey(List,on_delete=models.CASCADE,related_name="curr_list")
    problem = models.ForeignKey(Problem,on_delete = models.CASCADE,related_name='curr_prob')
    description = models.TextField(max_length=400,default=" ")

    def __str__(self):
        return str(self.l) + str(self.problem)
    
class Solved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user")
    problem = models.ForeignKey(Problem,on_delete = models.CASCADE,related_name='prob')
    def __str__(self):
        return str(self.user.username) + "'s solve" 