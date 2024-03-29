# Generated by Django 3.1.4 on 2021-12-11 06:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lists', '0005_ladderstarted'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrolled',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('enroll_list',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='enroll_user',
                                   to='lists.list')),
                ('enroll_user',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='enroll_user',
                                   to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
