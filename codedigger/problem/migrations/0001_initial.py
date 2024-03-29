# Generated by Django 3.1.4 on 2020-12-18 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='atcoder_contest',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('contestId', models.CharField(max_length=50)),
                ('name', models.CharField(blank=True,
                                          max_length=200,
                                          null=True)),
                ('startTime',
                 models.CharField(blank=True, max_length=20, null=True)),
                ('duration',
                 models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('name', models.CharField(blank=True,
                                          max_length=200,
                                          null=True)),
                ('prob_id', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=200)),
                ('tags', models.CharField(blank=True,
                                          max_length=500,
                                          null=True)),
                ('contest_id',
                 models.CharField(blank=True, max_length=50, null=True)),
                ('index', models.CharField(blank=True,
                                           max_length=20,
                                           null=True)),
                ('rating',
                 models.CharField(blank=True, max_length=10, null=True)),
                ('platform',
                 models.CharField(choices=[('F', 'Codeforces'),
                                           ('C', 'Codechef'), ('S', 'Spoj'),
                                           ('U', 'Uva'), ('A', 'Atcoder')],
                                  max_length=1)),
                ('difficulty',
                 models.CharField(blank=True,
                                  choices=[('B', 'Beginner'), ('E', 'Easy'),
                                           ('M', 'Medium'), ('H', 'Hard'),
                                           ('S', 'Super-Hard'),
                                           ('C', 'Challenging')],
                                  max_length=1,
                                  null=True)),
                ('editorial',
                 models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
