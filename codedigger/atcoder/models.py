from django.db import models

# Create your models here.
class atcoder_contest(models.Model):
    contestId = models.CharField(max_length=50, db_index=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    startTime = models.CharField(max_length=20, blank=True, null=True)
    duration = models.CharField(max_length=10, blank=True, null=True)
