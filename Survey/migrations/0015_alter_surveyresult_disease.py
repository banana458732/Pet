# Generated by Django 4.0 on 2024-11-21 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Survey', '0014_surveyresult_age_range'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyresult',
            name='disease',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
