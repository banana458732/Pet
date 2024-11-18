# Generated by Django 4.0 on 2024-11-14 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0025_alter_petimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='type',
            field=models.CharField(choices=[('犬', '犬'), ('猫', '猫')], default='', max_length=10, verbose_name='種類'),
        ),
    ]
