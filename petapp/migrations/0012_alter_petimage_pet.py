# Generated by Django 4.0 on 2024-11-06 03:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0011_alter_pet_color_alter_pet_size_alter_pet_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petimage',
            name='pet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='petapp.pet'),
        ),
    ]
