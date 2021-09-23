from django.db import models
from user.models import User
from problem.models import Problem
from codeforces.models import user as CodeforcesUser

# Create your models here.
class Contest(models.Model):
	owner  = models.ForeignKey(to=User,related_name='contest_owner',on_delete=models.CASCADE)
	name =  models.CharField(max_length=100,blank = True,default=" ")
	problem  = models.ManyToManyField(Problem,through= 'ContestProblem',through_fields=('contest','problem'),related_name='contest_problem')
	participants  = models.ManyToManyField(User,through= 'ContestParticipation',through_fields=('contest','user'),related_name='contest_participants')
	duration  = models.DurationField(default = 7200000000)
	created_at  = models.DateTimeField(auto_now_add = True)
	startTime  = models.DateTimeField()
	# numberOfProblem = models.IntegerField(default = 5)
	# platform = models.CharField(max_length = 5,blank=True, default = "F")
	# tag = models.CharField(max_length = 500 , blank=True, default = "")
	# rating = models.IntegerField(default = 1200)
	# difficulty = models.CharField(max_length = 1 , choices = DIFFICULTY , default='R')
	# isMentorOn = models.BooleanField(default = False)
	isTeam = models.BooleanField(default = False)
	# isProblem = models.BooleanField(default = False)
	isResult = models.BooleanField(default = False)
	# isGym = models.BooleanField(default=False)

	def __str__(self):
		return self.name

class ContestProblem(models.Model):
	contest  = models.ForeignKey(Contest,on_delete=models.CASCADE)
	problem  = models.ForeignKey(Problem,on_delete=models.CASCADE)
	index  = models.IntegerField()

	def __str__(self):
		return self.problem.prob_id + ' is there in ' + self.contest.name


class ContestParticipation(models.Model):
	contest  = models.ForeignKey(Contest,on_delete=models.CASCADE)
	user =  models.ForeignKey(User,on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username + ' is participating in '+ self.contest.name


class ContestResult(models.Model):
	contestProblem =  models.ForeignKey(ContestProblem, on_delete = models.CASCADE)
	contestParticipation =  models.ForeignKey(ContestParticipation , on_delete = models.CASCADE)
	submissionTime =  models.DurationField()
	penalty =  models.IntegerField()

	def __str__(self):
		return self.contestParticipation.user.username +  " " + str(self.penalty)+" " + self.contestProblem.problem.prob_id + " " + self.contestProblem.contest.name


# These Models are to deal with Codeforces Group Contest 
# And to store Submission of these contest
# Example - Short Code Contest Format

class CodeforcesContest(models.Model):
	contestId = models.IntegerField()
	groupId = models.CharField(max_length = 20, blank = True, default=" ")
	name = models.CharField(max_length = 100, blank = True, default=" ")
	Type = models.CharField(max_length = 100)
	showOnlyOfficial = models.BooleanField()
	nproblems = models.IntegerField()

	def __str__(self):
		return self.name

class CodeforcesContestParticipation(models.Model):
	contest = models.ForeignKey(CodeforcesContest, on_delete = models.CASCADE)
	user = models.ForeignKey(CodeforcesUser, on_delete = models.CASCADE)
	participantId = models.IntegerField()
	isOfficial = models.BooleanField()
	isVirtual = models.BooleanField()

	def __str__(self):
		return self.user.handle + " participated in " + self.contest.name

class CodeforcesContestSubmission(models.Model):
	participant = models.ForeignKey(CodeforcesContestParticipation, on_delete = models.CASCADE)
	isSolved = models.BooleanField(null = True)
	submissionId = models.IntegerField(null = True)
	problemIndex = models.IntegerField(null = True)
	penalty = models.IntegerField(null = True)
	lang = models.CharField(max_length = 50, null = True)

	def __str__(self):
		if self.isSolved : 
			return self.participant.user.handle + " solved " + self.participant.contest.name + " - " + str(self.problemIndex)
		else :
			return self.participant.user.handle + " not solved " + self.participant.contest.name + " - " +str(self.problemIndex)

# END of Models Codeforces Contest