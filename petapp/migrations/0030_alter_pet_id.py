# Generated by Django 4.0 on 2024-11-29 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0029_alter_pet_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]