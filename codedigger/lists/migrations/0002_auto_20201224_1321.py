# Generated by Django 3.1.4 on 2020-12-24 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='slug',
            field=models.SlugField(blank=True, default=' ', max_length=20),
        ),
    ]