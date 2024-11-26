# Generated by Django 4.0 on 2024-11-27 00:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0028_remove_pet_syu_pet_kinds_alter_pet_age_and_more'),
        ('accounts', '0004_alter_customuser_phone_number'),
        ('Survey', '0021_delete_matchinghistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='petapp.pet')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customuser')),
            ],
        ),
    ]
