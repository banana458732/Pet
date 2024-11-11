# Generated by Django 4.0 on 2024-11-07 05:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0020_alter_pet_phone_number_alter_phonenumber_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='phone_number',
            field=models.CharField(max_length=15, null=True, validators=[django.core.validators.RegexValidator('^\\d{10,15}$', '電話番号は数字のみで、10～15桁にしてください。')]),
        ),
    ]
