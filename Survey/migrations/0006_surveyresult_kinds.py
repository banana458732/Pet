# Generated by Django 4.0 on 2024-11-19 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Survey', '0005_remove_surveyhistory_matched_pet_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyresult',
            name='kinds',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]