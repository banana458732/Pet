# Generated by Django 4.0 on 2024-11-19 01:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Survey', '0002_surveyresult_living_environment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='surveyresult',
            name='living_environment',
        ),
    ]