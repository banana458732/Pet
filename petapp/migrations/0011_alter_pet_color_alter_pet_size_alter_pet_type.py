# Generated by Django 4.0 on 2024-11-06 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0010_remove_pet_image_petimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='color',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='pet',
            name='size',
            field=models.CharField(choices=[('large', '大型'), ('medium', '中型'), ('small', '小型')], default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='pet',
            name='type',
            field=models.CharField(choices=[('dog', '犬'), ('cat', '猫')], default='', max_length=10),
        ),
    ]
