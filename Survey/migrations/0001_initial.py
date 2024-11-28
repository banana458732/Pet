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
