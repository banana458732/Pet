# Generated by Django 4.0 on 2024-11-07 03:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0018_remove_pet_phone_number_phonenumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='phonenumber',
            name='number',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='phonenumber',
            name='pet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phone_numbers', to='petapp.pet'),
        ),
    ]
