# Generated by Django 4.0 on 2024-11-07 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0015_remove_pet_shelter_delete_shelter'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
