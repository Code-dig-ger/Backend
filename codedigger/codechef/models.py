from django.db import models
from problem.models import Problem


# Create your models here.
class CodechefContest(models.Model):
    name = models.CharField(max_length=200)
    contestId = models.CharField(max_length=10, db_index=True)
    duration = models.IntegerField(blank=True, null=True)
    startTime = models.CharField(blank=True, null=True, max_length=100)
    division = models.CharField(blank=True, null=True, max_length=5)
    url = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.contestId


class CodechefContestProblems(models.Model):
    contest = models.ForeignKey(CodechefContest, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    def __str__(self):
        return self.problem.prob_id
