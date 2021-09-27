from django.db import models
import random


class Problem(models.Model):
    PLATFORM = (('F', 'Codeforces'), ('C', 'Codechef'), ('S', 'Spoj'),
                ('U', 'Uva'), ('A', 'Atcoder'))
    DIFFICULTY = (('B', 'Beginner'), ('E', 'Easy'), ('M', 'Medium'),
                  ('H', 'Hard'), ('S', 'Super-Hard'), ('C', 'Challenging'))
    name = models.CharField(max_length=200, blank=True, null=True)
    prob_id = models.CharField(max_length=50, db_index=True)
    url = models.CharField(max_length=200)
    tags = models.CharField(max_length=500, blank=True, null=True)
    contest_id = models.CharField(max_length=50, blank=True, null=True)
    index = models.CharField(max_length=20, blank=True, null=True)
    rating = models.IntegerField(null=True, blank=True)
    platform = models.CharField(max_length=1, choices=PLATFORM)
    difficulty = models.CharField(max_length=1,
                                  choices=DIFFICULTY,
                                  blank=True,
                                  null=True)
    editorial = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.prob_id

    def save(self, **kwargs):
        if self.rating is not None:
            super(Problem, self).save()
        else:
            if self.difficulty is None:
                self.rating = random.randint(800, 4000)
                super(Problem, self).save()
            else:
                if self.difficulty == 'B':
                    self.rating = random.randint(800, 1100)

                elif self.difficulty == 'E':
                    self.rating = random.randint(1100, 1500)

                elif self.difficulty == 'M':
                    self.rating = random.randint(1500, 1800)

                elif self.difficulty == 'H':
                    self.rating = random.randint(1800, 2100)

                elif self.difficulty == 'S':
                    self.rating = random.randint(2100, 2600)

                else:
                    self.rating = random.randint(2600, 4000)

            super(Problem, self).save()


class atcoder_contest(models.Model):
    contestId = models.CharField(max_length=50, db_index=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    startTime = models.CharField(max_length=20, blank=True, null=True)
    duration = models.CharField(max_length=10, blank=True, null=True)
