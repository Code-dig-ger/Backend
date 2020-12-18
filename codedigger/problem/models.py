from django.db import models

class Problem(models.Model):
    PLATFORM = (
        ('F' , 'Codeforces'),
        ('C' , 'Codechef'),
        ('S' , 'Spoj'),
        ('U' , 'Uva'),
        ('A' , 'Atcoder') 
    )
    DIFFICULTY = (
        ('B' , 'Beginner'),
        ('E' , 'Easy'),
        ('M' , 'Medium'),
        ('H' , 'Hard'),
        ('S' , 'Super-Hard'),
        ('C' , 'Challenging')
    )
    name = models.CharField(max_length=200 , blank = True , null = True)
    prob_id = models.CharField(max_length=50)
    url = models.CharField(max_length=200)
    tags = models.CharField(max_length = 500, blank = True , null= True)
    contest_id = models.CharField(max_length=50, blank = True , null = True)
    index = models.CharField(max_length=20, blank = True , null = True)
    rating = models.CharField(max_length=10, blank = True , null = True)
    platform = models.CharField(max_length = 1 ,choices = PLATFORM)
    difficulty = models.CharField(max_length = 1 , choices = DIFFICULTY , blank = True , null = True) 
    editorial = models.CharField(max_length = 200 , blank = True , null = True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class atcoder_contest(models.Model):
    contestId = models.CharField(max_length = 50)
    name = models.CharField(max_length = 200 , blank = True , null= True)
    startTime = models.CharField(max_length = 20 , blank = True , null = True)
    duration = models.CharField(max_length = 10 , blank = True , null = True)
    