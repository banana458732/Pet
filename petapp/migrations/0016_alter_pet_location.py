# Generated by Django 4.0 on 2025-01-31 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0015_pet_latitude_pet_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='location',
            field=models.CharField(default='', max_length=255, verbose_name='保護施設'),
        ),
    ]
