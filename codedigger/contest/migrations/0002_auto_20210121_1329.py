# Generated by Django 3.1.4 on 2021-01-21 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='duration',
            field=models.DurationField(default=7200),
        ),
    ]
