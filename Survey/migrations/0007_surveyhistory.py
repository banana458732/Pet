# Generated by Django 4.0 on 2024-11-18 01:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0025_alter_petimage_image'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('Survey', '0006_delete_surveyhistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('matched_pet', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='survey_histories', to='petapp.pet')),
                ('survey_result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_histories', to='Survey.surveyresult')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_history', to='auth.user')),
            ],
        ),
    ]
