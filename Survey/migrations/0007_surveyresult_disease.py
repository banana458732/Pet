# Generated by Django 4.0 on 2024-11-19 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Survey', '0006_surveyresult_kinds'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyresult',
            name='disease',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
