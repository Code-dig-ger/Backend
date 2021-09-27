from django.db import models
from django.template.defaultfilters import slugify
from user.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    slug = models.CharField(max_length=55, unique=True)

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save()


class Blog(models.Model):
    STATUS = (
        ('0', 'Draft'),
        ('1', 'Pending'),
        ('2', 'Published')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=110, unique=True)
    body = models.CharField(max_length=5000, blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS, default='0')
    views = models.IntegerField(default=0)
    meta_title = models.CharField(max_length=100, blank=True, null=True)
    meta_desc = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    youtube_link = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.slug

    def save(self, **kwargs):
        self.slug = slugify(self.title)
        super(Blog, self).save()
