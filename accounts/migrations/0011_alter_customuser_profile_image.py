# Generated by Django 4.0 on 2024-11-28 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_customuser_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(blank=True, default='profile_images/ダウンロード3.jpeg', null=True, upload_to='profile_images/'),
        ),
    ]