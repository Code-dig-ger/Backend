from django.db import models
from django.db.models.fields import related
from problem.models import Problem
from user.models import User
from django.template.defaultfilters import slugify
import time
from django.dispatch import receiver
from django.db.models.signals import post_save

TYPE_CHOICES = (
    ("1", "List"),
    ("2", "Ladder"),
    ("3", "Both"),
)


class List(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    problem = models.ManyToManyField(Problem,
                                     through='ListInfo',
                                     through_fields=(
                                         'p_list',
                                         'problem',
                                     ),
                                     related_name='problem')
    name = models.CharField(max_length=100, default=" ")
    description = models.TextField(max_length=400, blank=True, null=True)
    isAdmin = models.BooleanField(default=False)
    isTopicWise = models.BooleanField(default=True)
    type_list = models.CharField(max_length=1,
                                 choices=TYPE_CHOICES,
                                 default='1')
    slug = models.SlugField(unique=True, max_length=35, blank=True)
    public = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        strtime = "".join(str(time.time()).split("."))
        if not self.isAdmin:
            self.type_list = '1'
            if len(self.name) > 30:
                string = "%s-%s" % (self.name[:30], self.owner.id)
                self.slug = slugify(string)
                super(List, self).save()
            else:
                string = "%s-%s" % (self.name, self.owner.id)
                self.slug = slugify(string)
                super(List, self).save()
        else:
            self.public = True
            if len(self.name) > 30:
                string = "%s" % (self.name[:30])
                self.slug = slugify(string)
                super(List, self).save()
            else:
                string = "%s" % (self.name)
                self.slug = slugify(string)
                super(List, self).save()

    @receiver(post_save, sender=User)
    def create_List(sender, instance, created, **kwargs):
        if created:
            List.objects.create(
                owner=instance,
                name="Upsolve",
                description=
                "Problems which you could not solve during a contest which you can solve now",
                isAdmin=instance.is_staff,
                isTopicWise=True,
                type_list='1',
                public=False,
            )
            List.objects.create(
                owner=instance,
                name="TO-DO",
                description=
                "Problems in which you have a doubt or want to solve afterwards",
                isAdmin=instance.is_staff,
                isTopicWise=True,
                type_list='1',
                public=False,
            )


class ListInfo(models.Model):
    p_list = models.ForeignKey(List,
                               on_delete=models.CASCADE,
                               related_name="curr_list")
    problem = models.ForeignKey(Problem,
                                on_delete=models.CASCADE,
                                related_name='curr_prob')
    description = models.TextField(max_length=400, blank=True, null=True)

    def __str__(self):
        return str(self.p_list) + " " + str(self.problem.prob_id)


class Solved(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="user")
    problem = models.ForeignKey(Problem,
                                on_delete=models.CASCADE,
                                related_name='prob')

    def __str__(self):
        return str(self.user.username) + " " + str(self.problem.name)


class ListExtraInfo(models.Model):
    curr_list = models.ForeignKey(List,
                                  on_delete=models.CASCADE,
                                  related_name="curr_list_extra")
    difficulty = models.IntegerField(null=True, blank=True)
    video_link = models.CharField(max_length=200, null=True, blank=True)
    contest_link = models.CharField(max_length=200, null=True, blank=True)
    editorial = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.curr_list.name + "'s extra info"


class LadderStarted(models.Model):
    ladder_user = models.ForeignKey(User,
                                    on_delete=models.CASCADE,
                                    related_name="ladder_user")
    ladder = models.ForeignKey(List,
                               on_delete=models.CASCADE,
                               related_name="ladder")

    def __str__(self):
        return self.ladder.name + " started by " + self.ladder_user.username


class Enrolled(models.Model):
    enroll_user = models.ForeignKey(User,
                                    on_delete=models.CASCADE,
                                    related_name="enroll_user")
    enroll_list = models.ForeignKey(List,
                                    on_delete=models.CASCADE,
                                    related_name="enroll_list")

    def __str__(self):
        return self.enroll_list.slug


class Editor(models.Model):
    editor_user = models.ForeignKey(User,
                                    on_delete=models.CASCADE,
                                    related_name="editor_user")
    editor_list = models.ForeignKey(List,
                                    on_delete=models.CASCADE,
                                    related_name="editor_list")

    def __str__(self):
        return str(self.editor_user) + " can edit list " + str(
            self.editor_list)
