from django.db import models


class organization(models.Model):
    name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        db_index=True)

    def __str__(self):
        return self.name


class country(models.Model):
    name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        db_index=True)

    def __str__(self):
        return self.name


class contest(models.Model):
    TYPE = (
        ('R', 'Regular'),
        ('G', 'Gym')
    )
    name = models.CharField(max_length=200)
    contestId = models.CharField(max_length=10, db_index=True)
    duration = models.IntegerField(blank=True, null=True)
    startTime = models.IntegerField(blank=True, null=True)
    Type = models.CharField(max_length=1, choices=TYPE)
    isUpdated = models.BooleanField(default=False)

    def __str__(self):
        return self.contestId


class user(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True,)
    handle = models.CharField(max_length=50, unique=True, db_index=True)
    rating = models.IntegerField(blank=True, null=True)
    maxRating = models.IntegerField(blank=True, null=True)
    rank = models.CharField(max_length=50, blank=True, null=True)
    maxRank = models.CharField(max_length=50, blank=True, null=True)
    country = models.ForeignKey(
        country,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    organization = models.ForeignKey(
        organization,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    photoUrl = models.CharField(max_length=100, blank=True, null=True)
    contestRank = models.ManyToManyField(
        contest,
        through='user_contest_rank',
        through_fields=('user', 'contest')
    )

    def __str__(self):
        return self.handle


class user_contest_rank(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    contest = models.ForeignKey(contest, on_delete=models.CASCADE)
    worldRank = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.user.handle) + ' is participated in ' + \
            str(self.contest.contestId)
