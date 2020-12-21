from django.db import models
from problem.models import Problem
from user.models import User



class List(models.Model):
    owner = models.ForeignKey(to=User,on_delete=models.CASCADE)
    problem = models.ManyToManyField(Problem,related_name='problem')
    name = models.CharField(max_length=255,default=" ")
    description = models.TextField(max_length=400,default=" ")
    isAdmin = models.BooleanField(default=True)
    isTopicWise = models.BooleanField(default=True)
    isList = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class ListInfo(models.Model):   
    curr_list = models.ForeignKey(List,on_delete=models.CASCADE,related_name="curr_list")
    problem = models.ForeignKey(Problem,on_delete = models.CASCADE,related_name='curr_prob')
    description = models.TextField(max_length=400,default=" ")

    def __str__(self):
        return str(self.curr_list) + str(self.problem)
    
class Solved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user")
    problem = models.ForeignKey(Problem,on_delete = models.CASCADE,related_name='prob')
    def __str__(self):
        return str(self.user.username) + "'s solve" 