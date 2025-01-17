# Generated by Django 4.0 on 2025-01-16 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_customuser_address1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='adrress2',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='建物名'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='street_address',
            field=models.CharField(blank=True, max_length=6, verbose_name='番地'),
        ),
    ]
