from django.db import models

class organization(models.Model):
	name = models.CharField(max_length=50 , blank=True, null=True,)
	current = models.CharField(max_length=6)
	total = models.CharField(max_length=6)
	def __str__(self):
		return self.name

class country(models.Model):
	name = models.CharField(max_length=50 , blank=True, null=True,)
	current = models.CharField(max_length=6)
	total = models.CharField(max_length=6)
	def __str__(self):
		return self.name

class contest(models.Model):
	TYPE = (
		('R' , 'Regular'),
		('G' , 'Gym')
	)
	name = models.CharField(max_length=200)
	contestId = models.CharField(max_length=10)
	duration = models.CharField(max_length=50)
	startTime = models.CharField(max_length=50 , blank = True , null = True)
	participants = models.CharField(max_length=6 , blank = True , null = True)
	Type = models.CharField(max_length=1, choices=TYPE)

	def __str__(self):
		return self.name
    
class user(models.Model):
	name = models.CharField(max_length=100 , blank=True, null=True,)
	handle = models.CharField(max_length=50)
	rating = models.CharField(max_length=4)
	maxRating = models.CharField(max_length=4)
	rank = models.CharField(max_length=50)
	maxRank = models.CharField(max_length=50)
	worldRank = models.CharField(max_length=6 , blank=True, null=True,)
	countryRank = models.CharField(max_length=6, blank=True, null=True,)
	organizationRank = models.CharField(max_length=6, blank=True, null=True,)
	country = models.ForeignKey(country , on_delete=models.SET_NULL, blank=True, null=True,)
	organization = models.ForeignKey(organization , on_delete=models.SET_NULL, blank=True, null=True,)
	photoUrl = models.CharField(max_length=100)
	contestRank = models.ManyToManyField(
        contest,
        through='user_contest_rank',
        through_fields=('user', 'contest')
    )

	def __str__(self):
		return self.name

class user_contest_rank(models.Model):
	user = models.ForeignKey(user , on_delete=models.CASCADE)
	contest = models.ForeignKey(contest , on_delete=models.CASCADE)
	worldRank = models.CharField(max_length=6)
	countryRank = models.CharField(max_length=6 , blank = True , null = True)
	organizationRank = models.CharField(max_length=6 , blank = True , null = True)

	def __str__(self):
		return self.user.name + self.contest.name

class organization_contest_participation(models.Model):
	organization = models.ForeignKey(organization , on_delete=models.CASCADE)
	contest = models.ForeignKey(contest , on_delete=models.CASCADE)
	current = models.CharField(max_length=6)
	total = models.CharField(max_length=6)

	def __str__(self):
		return self.organization.name + self.contest.name

class country_contest_participation(models.Model):
	country = models.ForeignKey(country , on_delete=models.CASCADE)
	contest = models.ForeignKey(contest , on_delete=models.CASCADE)
	current = models.CharField(max_length=6)
	total = models.CharField(max_length=6)
	
	def __str__(self):
		return self.country.name + self.contest.name

