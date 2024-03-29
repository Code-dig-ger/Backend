# Generated by Django 3.1.4 on 2021-01-02 15:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50,
                                          null=True)),
                ('slug', models.CharField(max_length=55, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=110, unique=True)),
                ('body',
                 models.CharField(blank=True, max_length=5000, null=True)),
                ('status',
                 models.CharField(choices=[('0', 'Draft'), ('1', 'Pending'),
                                           ('2', 'Published')],
                                  default='0',
                                  max_length=1)),
                ('views', models.IntegerField(default=0)),
                ('meta_title',
                 models.CharField(blank=True, max_length=100, null=True)),
                ('meta_desc',
                 models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category',
                 models.ForeignKey(
                     blank=True,
                     null=True,
                     on_delete=django.db.models.deletion.SET_NULL,
                     to='blog.category')),
                ('user',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
