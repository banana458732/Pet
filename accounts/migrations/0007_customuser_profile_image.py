# Generated by Django 4.0 on 2024-11-28 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_customuser_contract_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(blank=True, default='profile_images/default.jpg', null=True, upload_to='profile_images/'),
        ),
    ]
