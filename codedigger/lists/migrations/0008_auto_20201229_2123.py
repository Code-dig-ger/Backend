# Generated by Django 3.1.4 on 2020-12-29 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0007_auto_20201224_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='description',
            field=models.TextField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='listinfo',
            name='description',
            field=models.TextField(blank=True, max_length=400, null=True),
        ),
    ]