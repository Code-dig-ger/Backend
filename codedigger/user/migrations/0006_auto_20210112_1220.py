# Generated by Django 3.1.4 on 2021-01-12 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20210112_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gurus',
            field=models.CharField(blank=True, default=',', max_length=300),
        ),
    ]