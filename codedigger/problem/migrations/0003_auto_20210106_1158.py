# Generated by Django 3.1.4 on 2021-01-06 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0002_auto_20210106_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='rating',
            field=models.IntegerField(null=True),
        ),
    ]
