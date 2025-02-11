# Generated by Django 4.0 on 2025-01-16 01:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0007_address_pet_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='post_code',
            field=models.CharField(default='', max_length=8, validators=[django.core.validators.RegexValidator('^\\d{3}-\\d{4}$', '郵便番号は「XXX-XXXX」の形式で入力してください。')], verbose_name='郵便番号'),
        ),
        migrations.AlterField(
            model_name='pet',
            name='address',
            field=models.CharField(default='', max_length=255, verbose_name='住所'),
        ),
        migrations.DeleteModel(
            name='Address',
        ),
    ]
