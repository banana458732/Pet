# Generated by Django 4.0 on 2024-10-25 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0005_alter_pet_inuneko_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='syu',
            field=models.CharField(default='不明', max_length=100),
        ),
    ]