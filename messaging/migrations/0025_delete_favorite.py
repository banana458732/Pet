# Generated by Django 4.0 on 2024-11-27 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0024_merge_0020_merge_20241126_0930_0023_favorite'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Favorite',
        ),
    ]