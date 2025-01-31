# Generated by Django 4.0 on 2025-01-31 06:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_customuser_post_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(max_length=15, validators=[django.core.validators.RegexValidator('^[0-9]{10,11}$', '電話番号は半角数字のみで、10,11桁までにしてください。')], verbose_name='電話番号'),
        ),
    ]
