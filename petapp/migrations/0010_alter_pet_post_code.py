# Generated by Django 4.0 on 2025-01-16 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0009_alter_pet_phone_number_alter_pet_post_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='post_code',
            field=models.CharField(default='', max_length=10, verbose_name='郵便番号'),
        ),
    ]
