# Generated by Django 4.0 on 2024-12-02 02:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0030_alter_pet_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='age',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(15)], verbose_name='歳'),
        ),
    ]
