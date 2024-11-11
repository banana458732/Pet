# Generated by Django 4.0 on 2024-11-07 03:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0017_alter_pet_size_alter_pet_type_alter_survey_pet_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pet',
            name='phone_number',
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=20)),
                ('pet', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='phone_number', to='petapp.pet')),
            ],
        ),
    ]