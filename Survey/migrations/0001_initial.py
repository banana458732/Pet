<<<<<<< HEAD
# Generated by Django 4.0 on 2024-11-27 07:12
=======
<<<<<<< HEAD
# Generated by Django 4.0 on 2024-11-28 01:02
=======
# Generated by Django 4.0 on 2024-11-27 07:12
>>>>>>> 96d2f2ca89e30a957ae172d991cd799a1d3b7107
>>>>>>> 3bad6f4af4f273e5b9070a43c7711c98027825b9

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pet_type', models.CharField(blank=True, max_length=255)),
                ('size', models.CharField(blank=True, max_length=255)),
                ('color', models.CharField(blank=True, max_length=255)),
                ('age', models.CharField(blank=True, max_length=255)),
                ('pet_personality', models.CharField(blank=True, max_length=255)),
                ('activity_level', models.CharField(blank=True, max_length=255)),
                ('pet_size_preference', models.CharField(blank=True, max_length=255)),
                ('additional_requests', models.TextField(blank=True)),
                ('kinds', models.CharField(blank=True, max_length=255)),
                ('disease', models.CharField(blank=True, default='', max_length=255)),
                ('sex', models.CharField(blank=True, max_length=255)),
                ('image_urls', models.TextField(blank=True)),
                ('age_range', models.CharField(blank=True, max_length=255)),
            ],
        ),
    ]
