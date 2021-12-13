from django.db import models
from problem.models import Problem
import datetime


# Create your models here.
class CodechefContest(models.Model):

    name = models.CharField(max_length=200)
    contestId = models.CharField(max_length=10, db_index=True)
    duration = models.IntegerField(blank=True, null=True)
    startTime = models.DateTimeField(blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.contestId


class CodechefContestProblems(models.Model):
    contest = models.ForeignKey(CodechefContest, blank = True,on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, blank = True,on_delete=models.CASCADE)

    def __str__(self):
        return self.problem.prob_id


class User(models.Model):
    username = models.CharField(max_length=50)
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    stars = models.IntegerField(blank=True, null=True, default=0)
    handle = models.CharField(max_length=50, unique=True, db_index=True)
    rating = models.IntegerField(blank=True, null=True, default=0)
    maxRating = models.IntegerField(blank=True, null=True, default=0)
    country = models.CharField(max_length=50, blank=True)
    country_rank = models.IntegerField(blank=True, null=True, default=0)    
    global_rank = models.IntegerField(blank=True, null=True, default=0)    
    def __str__(self):
        return self.handle