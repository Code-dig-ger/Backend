from django.db import models
from user.models import User
from problem.models import Problem

# Create your models here.
class Contest(models.Model):
	DIFFICULTY = (
        ('B' , 'Beginner'),
        ('E' , 'Easy'),
        ('M' , 'Medium'),
        ('H' , 'Hard'),
        ('S' , 'Super-Hard'),
        ('C' , 'Challenging'),
        ('R' , 'Random')
    )
	owner = models.ForeignKey(to=User,related_name='contest_owner',on_delete=models.CASCADE)
	name = models.CharField(max_length=100,blank = True,default=" ")
	problem = models.ManyToManyField(Problem,through= 'ContestProblem',through_fields=('contest','problem'),related_name='contest_problem')
	participants = models.ManyToManyField(User,through= 'ContestParticipation',through_fields=('contest','user'),related_name='contest_participants')
	duration = models.DurationField(default = 120)
	startTime = models.DateTimeField(auto_now_add=True)
	numberOfProblem = models.IntegerField(default = 5)
	platform = models.CharField(max_length = 5,blank=True, default = "F")
	tag = models.CharField(max_length = 500 , blank=True, default = "")
	rating = models.IntegerField(default = 1200)
	difficulty = models.CharField(max_length = 1 , choices = DIFFICULTY , default='R')
	isMentorOn = models.BooleanField(default = False)
	isTeam = models.BooleanField(default = False)
	isProblem = models.BooleanField(default = False)
	isResult = models.BooleanField(default = False)

	def __str__(self):
		return self.name

class ContestProblem(models.Model):
	contest = models.ForeignKey(Contest,on_delete=models.CASCADE)
	problem = models.ForeignKey(Problem,on_delete=models.CASCADE)

	def __str__(self):
		return self.problem.prob_id + ' is there in ' + self.contest.name

class ContestParticipation(models.Model):
	contest = models.ForeignKey(Contest,on_delete=models.CASCADE)
	user = models.ForeignKey(User,on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username + ' is participating in '+ self.contest.name

class ContestResult(models.Model):
	contest = models.ForeignKey(Contest , on_delete = models.CASCADE)
	problem = models.ForeignKey(Problem , on_delete = models.CASCADE)
	user = models.ForeignKey(User , on_delete = models.CASCADE)
	submissionTime = models.DateTimeField(auto_now_add=True)
	verdict = models.BooleanField(default = True)

