# Generated by Django 4.0 on 2024-11-20 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Survey', '0009_surveyresult_age_range'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='surveyresult',
            name='age_range',
        ),
        migrations.RemoveField(
            model_name='surveyresult',
            name='disease',
        ),
        migrations.RemoveField(
            model_name='surveyresult',
            name='sex',
        ),
    ]
